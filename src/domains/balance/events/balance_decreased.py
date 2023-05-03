from dataclasses import dataclass
from datetime import datetime

from src.domains.common import Event, EntityId


@dataclass
class BalanceDecreased(Event):
    decreased_amount: int
    balance_amount: int
    decreased_at: datetime
    balance_id: EntityId
