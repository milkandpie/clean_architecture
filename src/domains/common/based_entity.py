import uuid
from dataclasses import dataclass, asdict
from typing import List

from .based_event import BasedEvent


@dataclass
class BasedEntity:
    id: str

    def __init__(self):
        self.__events: List[BasedEvent] = []

    def get_events(self) -> List[BasedEvent]:
        return self.__events

    def add_event(self, event: BasedEvent):
        self.__events.append(event)

    def remove_event(self, event: BasedEvent):
        self.__events.remove(event)

    def clear_event(self):
        self.__events = []

    def to_dict(self) -> dict:
        return asdict(self)


class BaseEntityEvent(BasedEvent):
    def to_dict(self) -> dict:
        return self.__entity.to_dict()

    def __init__(self, entity: BasedEntity):
        self.__entity = entity
