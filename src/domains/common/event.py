import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import List

from .value_object import ValueObject, EntityId


class EventId(ValueObject):
    def __init__(self, _id: str = None):
        self.__id = _id or str(uuid.uuid4())

    def get_comparable(self):
        return self.__id


@dataclass
class Event(ABC):
    event_id: EventId
    aggregate_name: str
    aggregate_id: EntityId

    @classmethod
    def from_dict(cls, event_dict: dict):
        return cls(**event_dict)

    def to_dict(self) -> dict:
        return {'event_name': self.create_event_name(),
                **asdict(self)}

    def create_event_name(self) -> str:
        return ''.join('.%s' % c if c.isupper() else c
                       for c in self.__class__.__name__).strip('.').lower()


class EventHandleable(ABC):
    @abstractmethod
    def handle(self, event: Event):
        pass


@dataclass
class IntegrationEvent(Event):
    key: str = None
    payload: dict = field(default_factory=lambda: {})


class IntegrationEventHandled(ABC):

    @abstractmethod
    def add_integration_event(self, event: IntegrationEvent):
        pass

    @abstractmethod
    def get_integration_events(self) -> List[IntegrationEvent]:
        pass


class IntegrationEventHandler(IntegrationEventHandled):
    def __init__(self):
        self.__events: List[IntegrationEvent] = []

    def add_integration_event(self, event: IntegrationEvent):
        self.__events.append(event)

    def get_integration_events(self) -> List[IntegrationEvent]:
        return self.__events


@dataclass
class DelayedEvent(IntegrationEvent):
    delayed: int = 0


class DelayedEventHandled(ABC):
    @abstractmethod
    def add_delayed_event(self, event: DelayedEvent):
        pass

    @abstractmethod
    def get_delayed_events(self) -> List[DelayedEvent]:
        pass


class DelayedEventHandler(DelayedEventHandled):
    def __init__(self):
        self.__events: List[DelayedEvent] = []

    def add_delayed_event(self, event: DelayedEvent):
        self.__events.append(event)

    def get_delayed_events(self) -> List[DelayedEvent]:
        return self.__events
