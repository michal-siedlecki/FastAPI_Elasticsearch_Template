from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from core.rout.users import users_router
from core.rout.auth import auth_router
from core.rout.home import home_router


app = FastAPI(
    title="Base auth project", 
    openapi_url=f"{settings.API_VERSION}/openapi.json"
)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.APP_SECRET_KEY
)

app.include_router(auth_router, prefix=settings.API_VERSION)
app.include_router(users_router, prefix=settings.API_VERSION)
app.include_router(home_router, prefix=settings.API_VERSION)

