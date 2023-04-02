from abc import ABC, abstractmethod

from domains import Executable


class Repository(ABC):
    @abstractmethod
    async def create(self) -> Executable:
        pass

    @abstractmethod
    async def save(self, domain: Executable) -> bool:
        pass
