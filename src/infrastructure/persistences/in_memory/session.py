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
        if self.__db.get('events') is None:
            self.__db['events'] = []

        try:
            self.__db['events'].extend(events)
        except KeyError:
            raise
