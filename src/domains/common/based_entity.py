import uuid
from dataclasses import dataclass
from typing import List

from .based_event import BasedEvent


@dataclass
class BasedEntity:
    id: str = str(uuid.uuid4())

    def __init__(self):
        self.__events: List[BasedEvent] = []

    def add_event(self, event: BasedEvent):
        self.__events.append(event)

    def remove_event(self, event: BasedEvent):
        self.__events.remove(event)

    def clear_event(self):
        self.__events = []
