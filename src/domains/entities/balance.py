from dataclasses import dataclass

from src.domains.common import BasedEntity
from src.domains.exceptions import BalanceInsufficientException


@dataclass
class Balance(BasedEntity):
    amount: float = 0

    def increase(self, amount: float) -> float:
        self.amount += amount
        return self.amount

    def decrease(self, amount: float) -> float:
        if self.amount < amount:
            raise BalanceInsufficientException()

        self.amount -= amount
        return self.amount
