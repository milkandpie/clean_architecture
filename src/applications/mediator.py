from copy import deepcopy

from src.applications.account import AccountBalanceCreateHandler
from src.applications.balance import ToAnotherAggregateHandler
from src.applications.common import EventsMediator
from src.domains import (
    BalanceIncreased,
    BalanceDecreased,
    AccountRegistered,
    BalanceDecreasedFailed)
from .account import (
    AccountLoginCommand, AccountLoginService,
    AccountRegisterCommand, AccountRegisteringService)
from .balance import (
    BalanceTopUpCommand, BalanceTopUpService,
    BalanceDecreasingCommand, BalanceDecreasingService)
from .common import RepositoryInjector

_event_mediator = EventsMediator(
    {
        AccountRegistered: [AccountBalanceCreateHandler],
        BalanceIncreased: [ToAnotherAggregateHandler],
        BalanceDecreased: [],
        BalanceDecreasedFailed: [],
    }
)

_command_mediator = EventsMediator(
    {
        BalanceTopUpCommand: [BalanceTopUpService],
        BalanceDecreasingCommand: [BalanceDecreasingService],
        AccountLoginCommand: [AccountLoginService],
        AccountRegisterCommand: [AccountRegisteringService],
    }
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
