import os
from fastapi import Depends
from elasticsearch import Elasticsearch
from core.config import settings

ES = Elasticsearch(hosts=settings.ES_SERVER, basic_auth=(settings.ES_USER, settings.ES_PASSWORD))


def get_index():
    return os.getenv('ES_INDEX')


def _get_search_result(search):
    results = []
    d = dict(search.body)
    hits = d['hits']['hits']
    for i in hits:
        results.append(i["_source"])
    return results


def _get_id_result(search):
    results = []
    if not search.body:
        return results
    d = dict(search.body)
    hits = d['hits']['hits']
    for i in hits:
        results.append(i["_id"])
    return results


def get_all_users():
    query = {
        "match_all": {}
    }

    try:
        r = ES.search(index=get_index(), query=query, size=10000)
        users = _get_search_result(r)
    except Exception:
        return None
    return users


def _get_result_by_parameter(param: str, value: str):
    d = {
        "term": {
            f"{param}.keyword": {
                "value": f"{value}",
                "boost": 1.0
            }
        }}
    try:
        return ES.search(index=get_index(), query=d)
    except Exception as x:
        print(x)
        return None


def get_id_by_email(email: str):
    r = _get_result_by_parameter('email', email)
    if r:
        return _get_id_result(r)[0]
    return None


def get_user_by_email(email: str):
    r = _get_result_by_parameter('email', email)
    if not r:
        return None
    users = _get_search_result(r)
    if len(users) == 0:
        return None
    return users[0]


def create_user(user_json):
    try:
        ES.index(index=get_index(), document=user_json)
    except Exception as e:
        return False
    return True


def update_user(user_model, user_db_id: str):
    body = {
        "script": {
            "source": '''
            ctx._source.last_logged = params.last_logged;
            ctx._source.password_hash = params.password_hash;
            ctx._source.is_active = params.is_active;
            ctx._source.role_id = params.role_id
            ''',
            "lang": "painless",
            "params": user_model.dict()
        }
    }
    try:
        ES.update(index=get_index(), id=user_db_id, body=body)
    except Exception:
        return False
    return True


def delete_all_users():
    try:
        ES.indices.delete(index=get_index())
    except Exception:
        return False
    return True
