from abc import ABC, abstractmethod

from src.domains import Executable


class Repository(ABC):
    @abstractmethod
    async def create(self) -> Executable:
        pass

    @abstractmethod
    async def save(self, domain: Executable) -> bool:
        pass
