from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.domains.common import AggregateRoot, EntityId
from .constants import DECREASED, INCREASED
from .entities import BalanceAdjustment
from .events import (
    BalanceIncreased,
    BalanceDecreased,
    BalanceDecreasedFailed)


@dataclass
class Balance(AggregateRoot):
    amount: int
    account_id: EntityId
    balance_adjustments: List[BalanceAdjustment] = field(default_factory=lambda: [])

    def increase(self, amount: int,
                 increased_at: datetime = None,
                 comment: str = None,
                 number: int = 0) -> int:
        balance_adjustment = BalanceAdjustment(number, comment, amount,
                                               self.id, INCREASED,
                                               self.amount)
        self.balance_adjustments.append(balance_adjustment)
        self.add_event(BalanceIncreased(self.amount, amount, increased_at, self))

        self.amount += amount

        return True

    def decrease(self, amount: int,
                 decreased_at: datetime = None,
                 comment: str = None,
                 number: int = 0) -> int:
        if self.amount < amount:
            self.add_event(BalanceDecreasedFailed(self.amount, amount, decreased_at, self))
            return False

        balance_adjustment = BalanceAdjustment(number, comment, amount,
                                               self.id, DECREASED,
                                               self.amount)
        self.balance_adjustments.append(balance_adjustment)
        self.add_event(BalanceDecreased(self.amount, amount, decreased_at, self))

        self.amount -= amount

        return True
