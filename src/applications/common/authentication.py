from abc import ABC, abstractmethod


class PasswordEncoded(ABC):
    @abstractmethod
    def encode(self, raw: str):
        pass


class TokenEncoded(ABC):
    @abstractmethod
    def encode(self, data: dict):
        pass
