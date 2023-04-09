from abc import ABC, abstractmethod


class Command(ABC):
    pass


class CommandHandleable(ABC):
    @abstractmethod
    def handle(self):
        pass
