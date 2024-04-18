from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from starlette.config import Config
from starlette.requests import Request

authorization_router = APIRouter()

# config = Config(".env")  # read config from .env file
oauth = OAuth()


usosapi_base_url = "http://apps.usos.pw.edu.pl/"
usosapi_base_url_secure = "https://apps.usos.pw.edu.pl/"

oauth.register(
    name="usos",
    client_id="TQbmzC4s3FSSBLd5gWkq",
    client_secret="nhmmmJezLgkp6jk3LaF2nEtEvZFuKwWtN9FGwsqA",
    api_base_url="https://apps.usos.pw.edu.pl/",
    request_token_url="https://apps.usos.pw.edu.pl/services/oauth/request_token",
    authorize_url="https://apps.usos.pw.edu.pl/services/oauth/authorize",
    access_token_url="https://apps.usos.pw.edu.pl/services/oauth/access_token",
)


@authorization_router.route("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.usos.authorize_redirect(request, redirect_uri)


@authorization_router.route("/auth")
async def auth(request: Request):
    token = await oauth.usos.authorize_access_token(request)
    url = "services/users/user"
    resp = await oauth.usos.get(
        url, params={"fields": "student_programmes"}, token=token
    )
    print(resp.json())
    return RedirectResponse(url="/api/v1/subjects")
