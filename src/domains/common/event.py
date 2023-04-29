from abc import ABC, abstractmethod


class BasedEvent(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass
