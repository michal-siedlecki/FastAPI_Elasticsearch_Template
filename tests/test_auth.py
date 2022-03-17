import time
import core.data.search
from core.config import settings


def test_set_up(export_test_index, database):
    len(database)
    time.sleep(1)
    assert export_test_index


def test_get_users_list(client, database):
    response = client.get(
        f"{settings.API_VERSION}/users"
    )
    assert len(response.json()) == len(database)
    assert response.status_code == 200


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
