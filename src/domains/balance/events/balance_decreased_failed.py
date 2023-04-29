from dataclasses import dataclass
from datetime import datetime

from src.domains.common import BaseEntityEvent, Entity


@dataclass
class BalanceDecreasedFailed(BaseEntityEvent):
    def __init__(self, balance_amount: int, decreased_amount, executed_at: datetime, balance: Entity):
        super().__init__(balance)
        self.__decreased_amount = decreased_amount
        self.__balance_amount = balance_amount
        self.__executed_at = executed_at

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'decreased_amount': self.__decreased_amount,
            'balance_amount': self.__balance_amount,
            'executed_at': self.__executed_at
        }
