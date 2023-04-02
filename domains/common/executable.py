from abc import ABC, abstractmethod


class Executable(ABC):
    @abstractmethod
    def execute(self):
        pass
