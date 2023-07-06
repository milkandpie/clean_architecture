from dataclasses import dataclass
from datetime import datetime

from src.domains.common import DomainEvent


@dataclass
class BalanceDecreasedFailed(DomainEvent):
    decreased_amount: int
    balance_amount: int
    executed_at: datetime
