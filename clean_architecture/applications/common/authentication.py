from abc import ABC, abstractmethod
from dataclasses import dataclass


class PasswordEncoded(ABC):
    @abstractmethod
    def encode(self, raw: str):
        pass


@dataclass
class AuthenticationUser:
    email: str


@dataclass
class EncodeData:
    email: str


class TokenUtils(ABC):
    @abstractmethod
    def encode(self, data: EncodeData):
        pass

    @abstractmethod
    def decode(self, token: str) -> AuthenticationUser:
        pass
