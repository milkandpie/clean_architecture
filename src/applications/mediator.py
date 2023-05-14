from src.applications.common import EventsMediator
from src.domains import (
    BalanceIncreased,
    BalanceDecreased,
    AccountRegistered,
    BalanceDecreasedFailed)

from src.applications.balance import ToAnotherAggregateHandler
from src.applications.account import AccountBalanceCreateHandler

mediator = EventsMediator(
    {
        AccountRegistered: [AccountBalanceCreateHandler],
        BalanceIncreased: [ToAnotherAggregateHandler],
        BalanceDecreased: [],
        BalanceDecreasedFailed: [],
    }
)
