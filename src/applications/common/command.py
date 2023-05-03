from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.domains import Event, AggregateRoot
from .integrated_event import (
    IntegratedEvent,
    DelayedEvent)


@dataclass
class Command(ABC):
    pass


class CommandHandleable(ABC):
    def __init__(self):
        self.__events: List[IntegratedEvent] = []
        self.__delayed_events: List[DelayedEvent] = []

    @abstractmethod
    def handle(self, command: Command):
        pass

    def add_integrate(self, event: Event, aggregate: AggregateRoot,
                      key: str = None):
        self.__events.append(IntegratedEvent(event.create_event_name(),
                                             str(aggregate.__class__.__name__).lower(),
                                             aggregate.get_id(),
                                             event.to_dict(),
                                             key=key))

    def add_delayed(self, event: Event, aggregate: AggregateRoot,
                    key: str = None, delayed: int = None):
        self.__delayed_events.append(DelayedEvent(event.create_event_name(),
                                                  str(aggregate.__class__.__name__).lower(),
                                                  aggregate.get_id(),
                                                  event.to_dict(),
                                                  delayed=delayed,
                                                  key=key))

    def get_integrated_events(self) -> List[IntegratedEvent]:
        return self.__events

    def get_delayed_event(self) -> List[DelayedEvent]:
        return self.__delayed_events
