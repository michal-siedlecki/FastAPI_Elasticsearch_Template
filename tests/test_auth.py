import time
from jose import jwt
import core.data.search

from core.config import settings


def test_set_up(export_test_index, database):
    len(database)
    time.sleep(1)
    assert export_test_index


def test_create_user(client, create_user_data):
    response = client.post(
        f"{settings.API_VERSION}/register",
        json=create_user_data
    )
    time.sleep(1)
    assert response.status_code == 200
    assert 'created' in str(response.content)


def test_retrive_user_from_db(create_user_data):
    email = create_user_data.get('email')
    u = core.data.search.get_user_by_email(email)
    assert u.get('email') == email


def test_valid_token(client, create_user_data, token):
    payload = jwt.decode(token, settings.HS256, algorithms=["HS256"])
    email: str = payload.get("sub")
    assert email == create_user_data.get('email')
