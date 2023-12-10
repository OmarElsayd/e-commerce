import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from ..util.constant import (
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password( password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


class JwtAuth:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_MINUTES
        self.ALGORITHM = ALGORITHM
        self.JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
        self.JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

    def create_access_token(self, subject: Union[str, Any], expires_delta: timedelta = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any], expires_delta: timedelta = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt



