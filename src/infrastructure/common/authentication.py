from datetime import datetime, timedelta

from src.applications import PasswordEncoded
import jwt

from hashlib import md5


class MD5PasswordEncoder(PasswordEncoded):
    def encode(self, raw: str):
        return md5(raw.encode()).hexdigest()


class JWTTokenEncoder:
    def encode(self, data: dict):
        encoded_data = {
            **data,
            'exp': datetime.utcnow() + timedelta(minutes=EXPIRED_TIME)
        }
        return jwt.encode(encoded_data, SECRET_KEY, algorithm='HS256')
