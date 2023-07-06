from dataclasses import dataclass
from datetime import datetime

from src.domains.common import DomainEvent


@dataclass
class BalanceDecreased(DomainEvent):
    decreased_amount: int
    balance_amount: int
    decreased_at: datetime
