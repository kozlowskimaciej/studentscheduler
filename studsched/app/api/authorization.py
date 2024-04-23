from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client.apps import StarletteOAuth1App
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from sqlmodel import Session

from ..db.models import models
from ..db.queries import queries
from .base import get_db

authorization_router = APIRouter()


oauth = OAuth()


oauth.register(
    name="usos",
    client_id="TQbmzC4s3FSSBLd5gWkq",
    client_secret="nhmmmJezLgkp6jk3LaF2nEtEvZFuKwWtN9FGwsqA",
    api_base_url="https://apps.usos.pw.edu.pl/",
    request_token_url="https://apps.usos.pw.edu.pl/services/oauth/request_token",
    authorize_url="https://apps.usos.pw.edu.pl/services/oauth/authorize",
    access_token_url="https://apps.usos.pw.edu.pl/services/oauth/access_token",
)


@authorization_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.usos.authorize_redirect(request, redirect_uri)


@authorization_router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    usos: StarletteOAuth1App = oauth.create_client("usos")

    token = await usos.authorize_access_token(request)

    user = await usos.get(
        "services/users/user",
        params={"fields": "id|first_name|last_name"},
        token=token,
    )
    user = user.json()

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
    queries.add_user_info(db, user_info)

    url = request.url_for("subjects")
    return RedirectResponse(url=url)
