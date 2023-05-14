from typing import List


class InMemorySession:
    def __init__(self, db: dict):
        self.__db = db

    def get(self, key: str):
        try:
            return self.__db[key]
        except KeyError:
            return None

    def set(self, key: str, value):
        self.__db[key] = value
        return True

    def add_events(self, events: List[dict]):
        self._check_then_save('events', events)

    def add_integrate_events(self, events: List[dict]):
        self._check_then_save('integrate_events', events)

    def add_delayed_events(self, events: List[dict]):
        self._check_then_save('delayed_events', events)

    def _check_then_save(self, key: str, data: list):
        if self.__db.get(key) is None:
            self.__db[key] = []

        try:
            self.__db[key].extend(data)
        except KeyError:
            raise
