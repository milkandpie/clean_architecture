from abc import ABC, abstractmethod

from src.domains import Executable


class Repository(ABC):
    @abstractmethod
    async def create(self, command):
        pass

    @abstractmethod
    async def save(self, domain):
        pass
