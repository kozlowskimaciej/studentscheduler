"""Endpoints for getting version information."""

import asyncio
from typing import Any, Optional, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from starlette import status
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm.exc import NoResultFound
from starlette.websockets import WebSocket, WebSocketDisconnect

from ..chat.chat import create_chat_service
from ..chat.models.models import Channel, Message, MessageBase, MessageBody, UserBase
from ..configs import get_settings
from ..db.models.models import RequirementCreate, Subject, VersionResponse
from ..db.queries import queries
from ..db.session import engine
from ..version import __version__
from ..db.models import models
from ..db.queries import queries

base_router = APIRouter()


def get_db():
    with Session(engine) as session:
        yield session


@base_router.get("/version", response_model=models.VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return models.VersionResponse(version=__version__)


DatabaseDep = Annotated[Session, Depends(get_db)]


def get_current_user(request: Request, db: DatabaseDep):
    user_id = request.session.get("user_id")
    return db.get(models.User, user_id)


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]


@base_router.get("/subjects", response_model=list[models.Subject])
async def subjects(user: CurrentUserDep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No current user"
        )
    return queries.get_subjects(user)


@base_router.put("/subjects/{subject_id}/requirements")
async def replace_requirements(
    requirements: list[models.RequirementCreate],
    subject_id: int,
    db: DatabaseDep,
):
    try:
        queries.replace_requirements(db, subject_id, requirements)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found",
        )


@base_router.put("/subjects/{subject_id}/tasks")
async def replace_tasks(
    subject_id: int,
    tasks: list[models.TaskCreate],
    db: Session = Depends(get_db),
):
    try:
        queries.replace_tasks(db, subject_id, tasks)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found",
        )


redischat = None


@base_router.on_event("startup")
async def on_startup():
    global redischat
    redischat = create_chat_service(get_settings().REDIS_URL)


@base_router.on_event("shutdown")
async def on_shutdown():
    redischat.close()


def chat_service():
    assert redischat
    return redischat


async def authenticated_user():
    return UserBase(username="JakubStachowiak420")


@base_router.get(
    "/channels",
    response_model=list[Channel],
    dependencies=[Depends(authenticated_user)],
)
async def list_channels(chat=Depends(chat_service)):
    return await chat.get_channels()


async def channel_from_slug(
    channel_slug: str = Path(...), chat=Depends(chat_service)
) -> Channel:
    channel = await chat.get_channel(channel_slug)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="channel not found"
        )
    return channel


@base_router.get("/channels/{channel_slug}/messages", response_model=list[Message])
async def list_channel_messages(
    channel: Channel = Depends(channel_from_slug),
    chat=Depends(chat_service),
) -> list[Message]:
    return list(await chat.get_messages(channel.slug))


@base_router.post("/channels/{channel_slug}/messages", response_model=Message)
async def create_channel_message(
    user: UserBase = Depends(authenticated_user),
    channel: Channel = Depends(channel_from_slug),
    chat=Depends(chat_service),
    message: MessageBase = Body(...),
) -> MessageBase:
    return await chat.send_message(channel.slug, user, message)


@base_router.post(
    "/channels", response_model=Channel, dependencies=[Depends(authenticated_user)]
)
async def create_channel(chat=Depends(chat_service), channel: Channel = Body(...)):
    return await chat.create_channel(slug=channel.slug, name=channel.name)


@base_router.websocket("/channels/{channel_slug}/messages_ws")
async def channel_messages_ws(
    websocket: WebSocket,
    chat=Depends(chat_service),
    channel: Channel = Depends(channel_from_slug),
    user: Optional[UserBase] = Depends(authenticated_user),
):
    if not user:
        return
    async for message in chat.incoming_messages(
        channel_slug=channel.slug, read_timeout=1
    ):
        if message is ...:
            # No messages for some time, check if websocket is still active.
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            except asyncio.TimeoutError:
                continue
            except WebSocketDisconnect:
                # Client disconnected
                break
            else:
                continue
        await websocket.send_json(jsonable_encoder(message.dict()))
