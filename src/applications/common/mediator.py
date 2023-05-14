from abc import ABC, abstractmethod
from typing import List, Type, Dict

from src.applications.common import Repository
from src.domains import Event


class RepositoryInjector(ABC):
    @abstractmethod
    def get_concreate(self, repository_type: Type[Repository]):
        pass


class EventHandleable(ABC):
    def __init__(self, injector: RepositoryInjector = None):
        self._injector = injector

    @abstractmethod
    async def handle(self, event: Event):
        pass

    def set_injector(self, injector: RepositoryInjector):
        self._injector = injector


class EventsMediator:
    def __init__(self,
                 pairs: Dict[Type[Event], List[Type[EventHandleable]]] = None,
                 injector: RepositoryInjector = None):
        self.__repository_injector: RepositoryInjector = injector
        self.__event_handlers_pairs: Dict[Type[Event], List[Type[EventHandleable]]] = pairs or {}

    def register_event(self, event: Type[Event], handler: EventHandleable, handlers: List[EventHandleable] = None):
        handlers = handlers or []
        handlers.append(handler)

        if self.__event_handlers_pairs.get(event):
            self.__event_handlers_pairs[event].extend(handlers)
            return

        self.__event_handlers_pairs[event] = handlers

    async def handle(self, event: Event):
        handlers = self.__event_handlers_pairs.get(type(event))
        for handler_cls in handlers:
            handler = handler_cls(injector=self.__repository_injector)
            await handler.handle(event)

    def add_repository_injector(self, injector: RepositoryInjector):
        self.__repository_injector = injector
