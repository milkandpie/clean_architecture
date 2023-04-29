from dataclasses import dataclass, asdict
from typing import List

from .event import BasedEvent
from .value_object import EntityId, Comparable


@dataclass
class Entity(Comparable):
    id: EntityId

    def __init__(self):
        self.__events: List[BasedEvent] = []

    def get_comparable(self):
        return self.id.get_comparable()

    def get_events(self) -> List[BasedEvent]:
        return self.__events

    def add_event(self, event: BasedEvent):
        self.__events.append(event)

    def remove_event(self, event: BasedEvent):
        self.__events.remove(event)

    def clear_event(self):
        self.__events = []

    def __eq__(self, other: 'Entity'):
        return self.get_comparable() == other.get_comparable()

    def __repr__(self):
        return self.get_comparable()

    def to_dict(self) -> dict:
        return asdict(self)


class BaseEntityEvent(BasedEvent):
    def __init__(self, entity: Entity):
        self.__entity = entity

    def to_dict(self) -> dict:
        return {'id': str(self.__entity)}


class AggregateRoot(Entity):
    pass
