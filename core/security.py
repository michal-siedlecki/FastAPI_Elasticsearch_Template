import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from core.config import settings
from core.data import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.HS256, algorithm="HS256")
    return encoded_jwt


def decode_token(token):
    credentials_exception_no_user = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials user not found",
        headers={"WWW-Authenticate": "Bearer"},
    )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    credentials_exception_no_email = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials email not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.HS256, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception_no_email
    except JWTError:
        raise credentials_exception
    user = database.get_user_by_email(email)
    if user is None:
        raise credentials_exception_no_user
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
