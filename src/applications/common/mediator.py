from abc import ABC, abstractmethod
from typing import List, Type, Dict

from src.domains import Event
from logging import getLogger

log = getLogger(__name__)


class RepositoryInjector(ABC):
    @abstractmethod
    def get_concreate(self, repository_type):
        pass


class BasedRepositoryInjector(RepositoryInjector):
    def __init__(self, pairs: Dict = None):
        self.__repository_concreate_pairs = pairs or {}

    def get_concreate(self, repository_type):
        concreate = self.__repository_concreate_pairs.get(repository_type)
        if concreate is None:
            log.warning('Not registered abstract repository: %s', repository_type)

        return concreate

    def set_concreate(self, pairs: dict) -> 'BasedRepositoryInjector':
        self.__repository_concreate_pairs.update(pairs)
        return self

    def clone(self) -> 'BasedRepositoryInjector':
        return deepcopy(self)


class InMemoryRepositoryInjector(RepositoryInjector):
    def __init__(self, pairs: Dict = None):
        self.__repository_concreate_pairs = pairs or {}

    def get_concreate(self, repository_type):
        concreate = self.__repository_concreate_pairs.get(repository_type)
        if not concreate:
            raise Exception('Not registered abstract repository')

        return concreate


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
