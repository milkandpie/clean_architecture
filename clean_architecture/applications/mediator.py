from copy import deepcopy

from clean_architecture.applications.account import AccountBalanceCreateHandler
from clean_architecture.applications.balance import ToAnotherAggregateHandler
from clean_architecture.applications.common import EventsMediator
from clean_architecture.domains import (
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
