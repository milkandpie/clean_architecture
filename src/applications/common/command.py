from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.domains import (
    Event,
    DelayedEvent, DelayedEventHandled, DelayedEventHandler,
    IntegrationEvent, IntegrationEventHandled, IntegrationEventHandler)
from .mediator import EventHandleable


@dataclass
class Command(Event):
    pass


class CommandHandleable(IntegrationEventHandled, DelayedEventHandled, EventHandleable, ABC):
    def __init__(self):
        super().__init__()
        self.__delayed_handler = DelayedEventHandler()
        self.__integration_handler = IntegrationEventHandler()

    @abstractmethod
    def handle(self, command: Command):
        pass

    def add_delayed_event(self, event: DelayedEvent):
        self.__delayed_handler.add_delayed_event(event)

    def add_integration_event(self, event: IntegrationEvent):
        self.__integration_handler.add_integration_event(event)

    def get_delayed_events(self) -> List[DelayedEvent]:
        return self.__delayed_handler.get_delayed_events()

    def get_integration_events(self) -> List[IntegrationEvent]:
        return self.__integration_handler.get_integration_events()
