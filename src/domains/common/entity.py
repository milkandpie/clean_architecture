from typing import List

from .event import Event
from .value_object import EntityId, Comparable


class Entity(Comparable):
    def __init__(self, _id: EntityId = None):
        self.__id: EntityId = _id or EntityId()
        self.__events: List[Event] = []

    def get_comparable(self):
        return self.__id.get_comparable()

    def get_events(self) -> List[Event]:
        return self.__events

    def add_event(self, event: Event):
        self.__events.append(event)

    def remove_event(self, event: Event):
        self.__events.remove(event)

    def clear_events(self):
        self.__events = []

    def to_dict(self) -> dict:
        return {
            'id': str(self)
        }

    def get_id(self) -> EntityId:
        return self.__id

    def __eq__(self, other: Comparable):
        return self.get_comparable() == other.get_comparable()

    def __repr__(self):
        return self.get_comparable()


class AggregateRoot(Entity):
    pass

