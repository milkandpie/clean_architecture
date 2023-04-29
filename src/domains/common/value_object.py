from abc import ABC, abstractmethod


class Comparable(ABC):
    @abstractmethod
    def get_comparable(self):
        pass


class ValueObject(Comparable, ABC):

    def __eq__(self, other: 'ValueObject'):
        return self.get_comparable() == other.get_comparable()

    def __repr__(self):
        return self.get_comparable()


class EntityId(ValueObject):
    def __init__(self, _id: str):
        self.__id = _id

    def get_comparable(self):
        return self.__id
