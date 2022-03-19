import json
import os
import pytest

from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient
from core.config import settings
from core.main import app

api_version = settings.API_VERSION
server_host = settings.SERVER_HOST


@pytest.fixture(scope='session')
def export_test_index():
    os.environ['ES_INDEX'] = 'user_accounts_test'
    yield True
    os.unsetenv('ES_INDEX')


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='session')
def database():
    es = Elasticsearch(
        hosts=settings.ES_SERVER,
        basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
    )
    with open('scripts/db.json', 'r', encoding='utf-8') as f:
        d = json.loads(f.read())

    users = []
    emails = []
    for user in d.get('users').values():
        e = user.get('email')
        if e in emails:
            continue
        users.append(user)
        emails.append(e)

    for user in users:
        es.index(index=os.getenv('ES_INDEX'), document=user)
    yield users
    es.indices.delete(index=os.getenv('ES_INDEX'))


@pytest.fixture
def create_user_data():
    return {"email": "testuser", "password": "123", "role_id": 1, "is_active": "True"}


@pytest.fixture
def update_user_data():
    return {"email": "testuser", "password": "321", "role_id": 1, "is_active": "True"}


@pytest.fixture()
def token(client, create_user_data):
    response = client.post(f"{settings.API_VERSION}/token",
                           data={
                               "username": create_user_data.get('email'),
                               "password": create_user_data.get('password')
                           }
                           )
    return dict(response.json()).get('access_token')


@pytest.fixture()
def other_user():
    with open('scripts/db.json', 'r', encoding='utf-8') as f:
        d = json.loads(f.read())

    users = []
    emails = []
    for user in d.get('users').values():
        e = user.get('email')
        if e in emails:
            continue
        users.append(user)
        emails.append(e)

    return users[0]
