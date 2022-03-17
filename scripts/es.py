import os
import json
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '../.env'))


es = Elasticsearch(hosts=os.getenv('ES_SERVER'), basic_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')))

with open('db.json', 'r', encoding='utf-8') as f:
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
    es.index(index='user_accounts', document=user)

