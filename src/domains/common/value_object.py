import uuid
from abc import ABC, abstractmethod


class Comparable(ABC):
    @abstractmethod
    def get_comparable(self):
        pass


class ValueObject(Comparable, ABC):

    def __eq__(self, other: Comparable):
        return self.get_comparable() == other.get_comparable()

    def __repr__(self):
        return self.get_comparable()


class EntityId(ValueObject):
    def __init__(self, _id: str = None):
        self.__id = _id or str(uuid.uuid4())

    def get_comparable(self):
        return self.__id

    @staticmethod
    def create() -> ValueObject:
        return EntityId(str(uuid.uuid4()))
