from dataclasses import dataclass
from datetime import datetime

from clean_architecture.domains.common import DomainEvent


@dataclass
class BalanceDecreased(DomainEvent):
    decreased_amount: int
    balance_amount: int
    decreased_at: datetime
