from datetime import datetime

from src.domains.common import BaseEntityEvent, Entity
from dataclasses import dataclass


@dataclass
class BalanceDecreased(BaseEntityEvent):
    def __init__(self, balance_amount: int, decreased_amount: int, decreased_at: datetime, balance: Entity):
        super().__init__(balance)
        self.__decreased_amount = decreased_amount
        self.__balance_amount = balance_amount
        self.__decreased_at = decreased_at

    def create_event_name(self) -> str:
        return 'balance.decreased'

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'decreased_at': self.__decreased_at,
            'balance_id': str(self.get_entity()),
            'balance_amount': self.__balance_amount,
            'decreased_amount': self.__decreased_amount
        }
