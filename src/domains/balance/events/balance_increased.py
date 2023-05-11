from dataclasses import dataclass
from datetime import datetime

from src.domains.common import Event, EntityId


@dataclass
class BalanceIncreased(Event):
    increased_amount: int
    balance_amount: int
    increased_at: datetime

