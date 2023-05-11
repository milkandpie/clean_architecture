from dataclasses import dataclass
from datetime import datetime

from src.domains.common import Event


@dataclass
class BalanceDecreased(Event):
    decreased_amount: int
    balance_amount: int
    decreased_at: datetime
