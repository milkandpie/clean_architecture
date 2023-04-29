from abc import ABC
from typing import List

from .event import BasedEvent
from .value_object import EntityId, Comparable


class Entity(Comparable):
    def __init__(self, _id: EntityId = None):
        self.__id: EntityId = _id or EntityId()
        self.__events: List[BasedEvent] = []

    def get_comparable(self):
        return self.__id.get_comparable()

    def get_events(self) -> List[BasedEvent]:
        return self.__events

    def add_event(self, event: BasedEvent):
        self.__events.append(event)

    def remove_event(self, event: BasedEvent):
        self.__events.remove(event)

    def clear_event(self):
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


class BaseEntityEvent(BasedEvent, ABC):

    def __init__(self, entity: Entity):
        self.__entity = entity

    def get_entity(self) -> Entity:
        return self.__entity


class AggregateRoot(Entity):
    pass
