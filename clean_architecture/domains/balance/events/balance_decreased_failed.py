from dataclasses import dataclass
from datetime import datetime

from clean_architecture.domains.common import DomainEvent


@dataclass
class BalanceDecreasedFailed(DomainEvent):
    decreased_amount: int
    balance_amount: int
    executed_at: datetime
