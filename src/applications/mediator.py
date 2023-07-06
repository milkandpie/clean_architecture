from copy import deepcopy

from src.applications.common import EventsMediator
from .common import RepositoryInjector

_event_mediator = EventsMediator(
    {}
)

_command_mediator = EventsMediator(
    {}
)


class MediatorGetter:
    __mediators = {
        'event': _event_mediator,
        'command': _command_mediator
    }

    @classmethod
    def get_mediator(cls, ident: str, injector: RepositoryInjector = None) -> EventsMediator:
        try:
            mediator = deepcopy(cls.__mediators[ident])
            mediator.add_repository_injector(injector)
            return mediator
        except KeyError:
            raise Exception
