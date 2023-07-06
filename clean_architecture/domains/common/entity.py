from typing import List

from .event import (
    Event,
    DelayedEvent, DelayedEventHandled, DelayedEventHandler,
    IntegrationEvent, IntegrationEventHandled, IntegrationEventHandler)
from .value_object import EntityId, Comparable


class Entity(Comparable):
    def __init__(self, _id: EntityId = None):
        self.__id: EntityId = _id or EntityId()
        self.__events: List[Event] = []

    @property
    def id(self):
        return self.__id

    @property
    def events(self):
        return self.__events

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


class AggregateRoot(Entity,
                    IntegrationEventHandled, DelayedEventHandled):
    def __init__(self, _id: EntityId = None):
        super().__init__(_id)
        self.__delayed_handler = DelayedEventHandler()
        self.__integration_handler = IntegrationEventHandler()

    def add_integration_event(self, event: IntegrationEvent):
        self.__integration_handler.add_integration_event(event)

    def get_integration_events(self) -> List[IntegrationEvent]:
        return self.__integration_handler.get_integration_events()

    def add_delayed_event(self, event: DelayedEvent):
        self.__delayed_handler.add_delayed_event(event)

    def get_delayed_events(self) -> List[DelayedEvent]:
        return self.__delayed_handler.get_delayed_events()
