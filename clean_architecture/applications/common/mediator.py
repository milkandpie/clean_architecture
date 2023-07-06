import inspect
from abc import ABC, abstractmethod
from copy import deepcopy
from logging import getLogger
from typing import List, Type, Dict

from clean_architecture.domains import Event

log = getLogger(__name__)


class RepositoryInjector(ABC):
    @abstractmethod
    def get_concreate(self, repository_type):
        pass


class BasedRepositoryInjector(RepositoryInjector):
    def __init__(self, pairs: Dict = None):
        self.__repository_concreate_pairs = pairs or {}
        self.__repository_concreate_pairs[BasedRepositoryInjector] = self

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


class EventHandleable(ABC):
    @abstractmethod
    async def handle(self, event: Event):
        pass


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
        responses = []
        for handler_cls in handlers:
            handler = self.__init_params(handler_cls, injector_query=False)
            responses.append(await handler.handle(event))

        return responses

    def add_repository_injector(self, injector: RepositoryInjector):
        self.__repository_injector = injector

    def __init_params(self, type_hint, injector_query: bool = True):
        """

        :param type_hint: Object to get instance
        :param injector_query: If True, trigger query concreate instance on injector
        :return: Fully initialized instance
        """

        _initialing_cls = type_hint
        if injector_query:
            _initialing_cls = self.__repository_injector.get_concreate(type_hint)

        if not inspect.isclass(_initialing_cls):
            return _initialing_cls

        try:
            type_hints = _initialing_cls.__init__.__annotations__
            if not type_hints:
                return _initialing_cls()

        except AttributeError:
            # For class without specific __init__ method
            return _initialing_cls()

        initialing_params = {}
        for parameter_name, parameter_hint in type_hints.items():
            _parameter_instance = self.__init_params(parameter_hint)
            initialing_params[parameter_name] = _parameter_instance

        return _initialing_cls(**initialing_params)
