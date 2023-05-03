from abc import ABC, abstractmethod


class Event(ABC):
    def to_dict(self) -> dict:
        return {'event_name': self.create_event_name()}

    def from_dict(self, event_dict: dict):
        pass

    @abstractmethod
    def create_event_name(self) -> str:
        pass
