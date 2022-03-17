from core.mod import models
from core.data import search

def get_users():
    usr = search.get_all_users()
    if not usr:
        return []
    return [models.UserModel(**u) for u in usr]


def get_user_by_email(email: str):
    usr = search.get_user_by_email(email)
    if not usr:
        return None
    return models.UserModel(**usr)


def update_user(updated_user: models.UserModel):
    user_db_id = search.get_id_by_email(updated_user.email)
    if not user_db_id:
        return None
    return search.update_user(updated_user, user_db_id)


def add_user(new_user: models.UserModel):
    if get_user_by_email(new_user.email) is not None:
        return False
    return search.create_user(new_user.json())


def delete_users():
    return search.delete_all_users()
