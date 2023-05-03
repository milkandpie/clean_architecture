import uuid
from dataclasses import dataclass
from src.domains import ValueObject, EntityId


class EventId(ValueObject):
    def __init__(self, _id: str = None):
        self.__id = _id or str(uuid.uuid4())

    def get_comparable(self):
        return self.__id


@dataclass
class IntegratedEvent:
    event_name: str
    aggregate_name: str
    aggregate_id: EntityId
    payload: dict

    key: str = None
    event_id: EventId = EventId()


@dataclass
class DelayedEvent(IntegratedEvent):
    delayed: int = 0
