from src.applications.common import EventsMediator
from src.domains import (
    BalanceIncreased,
    BalanceDecreased,
    BalanceDecreasedFailed)

from .sample_event_handler import ToAnotherAggregateHandler

mediator = EventsMediator(
    {
        BalanceIncreased: [ToAnotherAggregateHandler],
        BalanceDecreased: [],
        BalanceDecreasedFailed: [],
    }
)
