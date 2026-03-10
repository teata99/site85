import os
from fastapi import APIRouter, Request, HTTPException
from pathlib import Path
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env03"
load_dotenv(dotenv_path=env_path)

router = APIRouter()

router.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@router.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    if user_info:
        request.session['user'] = dict(user_info)
        return RedirectResponse(url='/fastapi/fastapi03.html')
    
    return {"message": "Login failed"}

@router.get("/read")
async def read_user_info(request: Request):
    user = request.session.get('user')

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "name": user.get("name"),
        "email": user.get("email"),
        "picture": user.get("picture")
    }


@router.get("/hello")
def hello():
    return {"status": "FastAPI on Vercel is running!"}

