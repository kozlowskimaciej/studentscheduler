from authlib.integrations.starlette_client.apps import StarletteOAuth1App
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import datetime

from ..db.models import models
from ..db.queries import queries
from .base import get_db

authorization_router = APIRouter()


@authorization_router.get("/login")
async def login(request: Request):
    usos: StarletteOAuth1App = request.app.oauth.create_client("usos")

    request.session.clear()

    redirect_uri = request.url_for("auth")
    return await usos.authorize_redirect(request, redirect_uri)


@authorization_router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    usos: StarletteOAuth1App = request.app.oauth.create_client("usos")

    token = await usos.authorize_access_token(request)
    request.session["token"] = token

    user = await usos.get(
        "services/users/user",
        params={
            "fields": "student_number|first_name|middle_names|last_name|email"
        },
        token=token,
    )
    user = user.json()
    user["last_login"] = datetime.now()

    courses = await usos.get(
        "services/courses/user",
        params={"fields": "course_editions[course_id|course_name]"},
        token=token,
    )
    courses = courses.json()
    courses = [
        {"name": c["course_name"]["pl"], "code": c["course_id"]}
        for cs in courses["course_editions"].values()
        for c in cs
    ]

    user_info = models.UserInfo(user=user, courses=courses)
    db_user = queries.add_user_info(db, user_info)
    request.session["user_id"] = db_user.id

    url = request.url_for("subjects")
    return RedirectResponse(url=url)
