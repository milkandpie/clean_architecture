import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from .value_object import ValueObject


class DomainEventId(ValueObject):
    def __init__(self, _id: str = None):
        self.__id = _id or str(uuid.uuid4())

    def get_comparable(self):
        return self.__id


@dataclass
class Event(ABC):
    # TODO: Add identity
    # event_name: str
    # aggregate_id: str
    # aggregate_name: str
    # event_id: DomainEventId

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
