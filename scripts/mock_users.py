import json
import sys
import uuid
import bcrypt
from faker import Faker
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

f = Faker('pl_PL')

first_login = datetime(2022, 2, 1)
last_login = datetime(2022, 2, 21)
users = []

class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    last_logged: datetime = datetime.utcnow()
    password_hash: Optional[str]
    is_active: bool
    role_id: int


class Database(BaseModel):
    db_file: str
    users: dict[str, User]


def create_user() -> dict:
    return {
        "id": uuid.uuid4(),
        "email": f.email(),
        "last_logged": f.date_time_between(start_date=first_login, end_date=last_login),
        "password_hash": f.password(length=20),
        "is_active": 1,
        "role_id": 1
    }

def save(json_data, mock_file):
    file = open(mock_file, "w")
    file.write(json_data)
    file.close()
    return True


if __name__ == '__main__':
    mock_filename = "db.json"
    user_num = 0

    try:
        user_num = int(sys.argv[1])
    except ValueError:
        print("Value error - the parameter should be an int")
        quit()

    result = Database(db_file=mock_filename, users={})
    for _ in range(user_num):
        u = User(**create_user())
        result.users.update({u.email: u})

    if save(result.json(), mock_filename):
        print("mock created")
        quit()
    print("faled to create mock")
