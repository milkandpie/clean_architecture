from dataclasses import dataclass
from datetime import datetime

from clean_architecture.domains.common import DomainEvent


@dataclass
class BalanceIncreased(DomainEvent):
    increased_amount: int
    balance_amount: int
    increased_at: datetime
