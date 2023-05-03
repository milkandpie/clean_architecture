from dataclasses import dataclass
from datetime import datetime

from src.domains.common import Event, EntityId


@dataclass
class BalanceDecreasedFailed(Event):
    decreased_amount: int
    balance_amount: int
    executed_at: datetime
    balance_id: EntityId
