from datetime import datetime, timedelta
from hashlib import md5

import jwt

from clean_architecture.applications import (
    PasswordEncoded,
    TokenUtils,
    EncodeData,
    AuthenticationUser)
from .config import (EXPIRED_TIME, SECRET_KEY)


class MD5PasswordEncoder(PasswordEncoded):
    def encode(self, raw: str):
        return md5(raw.encode()).hexdigest()


class JWTTokenEncoder(TokenUtils):
    def __init__(self, secret_key: str = None, expired_time: int = None):
        self.__secret_key: str = secret_key or SECRET_KEY
        self.__expired_time: int = expired_time or EXPIRED_TIME

    def encode(self, data: EncodeData):
        encoded_data = {
            **{'email': data.email},
            'exp': datetime.utcnow() + timedelta(minutes=self.__expired_time)
        }
        return jwt.encode(encoded_data, self.__secret_key, algorithm='HS256')

    def decode(self, token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return AuthenticationUser(payload.get('email'))
