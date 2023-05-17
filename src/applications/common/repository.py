from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

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


@dataclass
class ListableParams:
    q: str
    page: int
    sort: str
    order: str
    limit: int
    filters: dict


@dataclass
class CountableParams:
    q: str
    filters: dict


@dataclass()
class GettableParams:
    id: str




class Listable(ABC):
    @abstractmethod
    async def list(self, param: ListableParams) -> List:
        pass


class Countable(ABC):
    @abstractmethod
    async def count(self, params: CountableParams) -> int:
        pass


class Gettable(ABC):
    @abstractmethod
    async def get(self, params: GettableParams):
        pass


class QueryRepository(Listable, Gettable, Countable):
    async def list(self, param: ListableParams):
        pass

    async def get(self, params: GettableParams):
        pass

    async def count(self, params: CountableParams):
        pass
