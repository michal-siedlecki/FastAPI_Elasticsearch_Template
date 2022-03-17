from typing import Optional
from fastapi import APIRouter, Depends
from core.mod.models import UserModel, UserModelPlain
from core.data.search import get_id_by_email
from core.rout.auth import get_current_user
from core.data import database

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
    # dependencies=[Depends(get_current_user)]
)


@users_router.get("/get_id")
async def get_user_id_by_email(email: str):
    return get_id_by_email(email)


@users_router.get("/")
async def user_get_all(email: Optional[str] = None):
    if email:
        return _get_user_by_email(email)
    return database.get_users()



@users_router.delete("/")
async def user_delete_all():
    database.delete_users()
    return {"message": "all users have been deleted"}


def _get_user_by_email(email: str):
    user = database.get_user_by_email(email)
    return user


@users_router.patch("/")
async def user_update(updated_user: UserModelPlain):
    user = database.get_user_by_email(updated_user.email)
    if not user:
        return {"message": "failed update user no user with this email"}
    user_id = user.id
    upt_user = UserModel(id=user_id, **updated_user.dict())
    upt_user.set_password_hash(updated_user.password)
    if not database.update_user(upt_user):
        return {"message": "failed update user"}
    return {"message": "user updated"}


@users_router.patch("/update_password")
async def user_update(updated_user: UserModelPlain):
    user = database.get_user_by_email(updated_user.email)
    if not user:
        return {"message": "failed update user no user with this email"}
    user.set_password_hash(updated_user.password)
    if not database.update_user(user):
        return {"message": "failed update user"}
    return {"message": "user updated"}
