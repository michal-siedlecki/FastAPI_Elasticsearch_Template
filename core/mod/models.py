import uuid
from datetime import datetime

from passlib.context import CryptContext
from pydantic import BaseModel, Field
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModelPlain(BaseModel):
    email: str
    password: str
    is_active: bool
    role_id: int


class UserModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    last_logged: datetime = datetime.utcnow()
    password_hash: Optional[str]
    is_active: bool
    role_id: int

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def set_password_hash(self, password):
        self.password_hash = pwd_context.hash(password)
