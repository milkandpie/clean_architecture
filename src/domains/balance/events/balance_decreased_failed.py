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

    def create_event_name(self) -> str:
        return 'balance.decreased.failed'

    def to_dict(self) -> dict:
        return {
            'decreased_amount': self.__decreased_amount,
            'balance_amount': self.__balance_amount,
            'balance_id': str(self.get_entity()),
            'executed_at': self.__executed_at
        }
