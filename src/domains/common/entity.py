from abc import ABC
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


class AggregateRoot(Entity):
    pass


class BaseEntityEvent(Event, ABC):

    def __init__(self, entity: Entity):
        self.__entity = entity

    def get_entity(self) -> Entity:
        return self.__entity

    def create_payload(self) -> dict:
        return {
            'model_id': str(self.__entity)
        }
