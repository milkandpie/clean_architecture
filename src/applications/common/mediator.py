from typing import List, Type, Dict

from src.domains import Event, EventHandleable


class EventsMediator:
    def __init__(self, pairs: Dict[Type[Event], List[Type[EventHandleable]]] = None):
        self.__event_handlers_pairs: Dict[Type[Event], List[Type[EventHandleable]]] = pairs or {}

    def register_event(self, event: Type[Event], handler: EventHandleable, handlers: List[EventHandleable] = None):
        handlers = handlers or []
        handlers.append(handler)

        if self.__event_handlers_pairs.get(event):
            self.__event_handlers_pairs[event].extend(handlers)
            return

        self.__event_handlers_pairs[event] = handlers

    def handle(self, event: Event):
        handlers = self.__event_handlers_pairs.get(type(event))
        for handler in handlers:
            handler().handle(event)


