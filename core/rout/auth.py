import os
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Form, Path
from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.config import settings
from core.mod.models import UserModelPlain, UserModel
from core.utils import send_reset_password_email
from core.security import decode_token, create_access_token, get_password_hash
from core.data import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION}/token")
oauth = OAuth(os.environ)
oauth.register(
    name='google',
    server_metadata_url=settings.CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

auth_router = APIRouter()


def authenticate_user(email: str, password: str):
    user = database.get_user_by_email(email)
    if user is None:
        return False
    if not user.verify_password(password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user


#:::::::::::::::::  ENDPOINTS :::::::::::::::::::::


@auth_router.post("/register")
async def user_create(new_user: UserModelPlain):
    user = UserModel(**new_user.dict())
    user.set_password_hash(new_user.password)
    if not database.add_user(user):
        return {"message": "failed create user"}
    return {"message": "user created"}

@auth_router.post('/token')
async def create_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    request.session.update({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.get('/token-google')
async def create_token_google(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user_data = await oauth.google.parse_id_token(request, access_token)
    email = user_data['email']
    user = database.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    request.session.update({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get('/login-google')
async def login(request: Request):
    redirect_uri = request.url_for('create_token_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f'{settings.API_VERSION}/login')


@auth_router.post("/reset-password-request")
async def request_password_reset(email: str = Form(...)):
    user = database.get_user_by_email(email)
    if not user:
        return {"message": "email with password reset link was not sent"}
    token = create_access_token(data={"sub": user.email})
    await send_reset_password_email(user.email, user.email, token)
    return {"message": f"email with password reset link was sent"}


@auth_router.post("/reset-password/")
def reset_password(token: str, new_password: str = Form(...)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.password_hash = hashed_password
    if database.update_user(user):
        return {"message": "Password updated successfully"}


@auth_router.get("/reset-password/{token}")
def password_reset(token: str = Path(...)):
    user = decode_token(token)
    if not user:
        return {"message": "user encoded with token does not exist"}
    return {"access_token": token, "token_type": "bearer"}
