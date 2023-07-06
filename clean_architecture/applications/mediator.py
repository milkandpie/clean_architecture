from copy import deepcopy

from clean_architecture.applications.common import EventsMediator
from .common import RepositoryInjector

_event_mediator = EventsMediator(
    {}
)

_command_mediator = EventsMediator(
    {}
)


class MediatorGetter:
    @classmethod
    def get_mediator(cls, ident: str, injector: RepositoryInjector = None) -> EventsMediator:
        try:
            mediators = cls._create_mediators()
            mediator = deepcopy(mediators[ident])
            mediator.add_repository_injector(injector)
            return mediator
        except KeyError:
            raise Exception

    @staticmethod
    def _create_mediators():
        return {
            'event': _event_mediator,
            'command': _command_mediator
        }