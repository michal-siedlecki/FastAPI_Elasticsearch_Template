from requests.structures import CaseInsensitiveDict
from core.config import settings


def test_get_users_list(client, create_user_data, token):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    response = client.get(
        f"{settings.API_VERSION}/users",
        headers=headers
    )
    assert len(response.json()) == 11
    assert response.status_code == 200


def test_failed_to_delete_all_users(client, create_user_data, token):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    response = client.delete(
        f"{settings.API_VERSION}/users/",
        headers=headers
    )
    assert response.status_code == 401
    assert 'no permissions' in str(response.content)


def test_failed_to_update_other_user(client, create_user_data, token, other_user, update_user_data):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    other_user_email = other_user.get('email')
    password = update_user_data.get('password')
    role_id = update_user_data.get('role_id')
    is_active = update_user_data.get('is_active')
    update_data = {
        "email": other_user_email,
        "password": password,
        "role_id": role_id,
        "is_active": is_active
    }

    response = client.patch(
        f"{settings.API_VERSION}/users/",
        headers=headers,
        json=update_data
    )

    assert response.status_code == 401
    assert 'no permissions' in str(response.content)


