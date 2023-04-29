from abc import ABC, abstractmethod

from src.domains import AggregateRoot
from .command import Command


class Repository(ABC):
    @abstractmethod
    async def create(self, command: Command) -> AggregateRoot:
        pass

    @abstractmethod
    async def save(self, domain: AggregateRoot) -> AggregateRoot:
        pass
