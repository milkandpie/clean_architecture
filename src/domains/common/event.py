from abc import ABC, abstractmethod


class BasedEvent(ABC):
    def to_dict(self) -> dict:
        return {'event_name': self.create_event_name()}

    @abstractmethod
    def create_event_name(self) -> str:
        pass
