from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.applications import PasswordEncoded
import jwt

from hashlib import md5
from .config import (EXPIRED_TIME, SECRET_KEY)


class MD5PasswordEncoder(PasswordEncoded):
    def encode(self, raw: str):
        return md5(raw.encode()).hexdigest()


@dataclass
class AuthenticationUser:
    email: str


@dataclass
class EncodeData:
    email: str
    secret_key: str
    expired_time: int


class TokenUtils(ABC):
    @abstractmethod
    def encode(self, data: EncodeData):
        pass

    @abstractmethod
    def decode(self, token: str) -> AuthenticationUser:
        pass


class JWTTokenEncoder(TokenUtils):
    def encode(self, data: EncodeData):
        encoded_data = {
            **{'email': data.email},
            'exp': datetime.utcnow() + timedelta(minutes=data.expired_time or EXPIRED_TIME)
        }
        return jwt.encode(encoded_data, data.secret_key or SECRET_KEY, algorithm='HS256')

    def decode(self, token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return AuthenticationUser(payload.get('email'))
