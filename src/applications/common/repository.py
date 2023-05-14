from abc import ABC, abstractmethod

from src.domains import AggregateRoot, DomainEvent
from .command import Command


class Repository(ABC):
    @abstractmethod
    async def create(self, command: Command) -> AggregateRoot:
        pass

    @abstractmethod
    async def save(self, domain: AggregateRoot) -> AggregateRoot:
        pass


class EventRepository(Repository, ABC):
    @abstractmethod
    async def create(self, event: DomainEvent) -> AggregateRoot:
        pass

    @abstractmethod
    async def save(self, domain: AggregateRoot) -> AggregateRoot:
        pass
