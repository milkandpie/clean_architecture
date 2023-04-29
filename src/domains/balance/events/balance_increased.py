from dataclasses import dataclass
from datetime import datetime

from src.domains.common import BaseEntityEvent, Entity


@dataclass
class BalanceIncreased(BaseEntityEvent):
    def __init__(self, balance_amount: int, increased_amount: int, increased_at: datetime, balance: Entity):
        super().__init__(balance)
        self.__increased_amount = increased_amount
        self.__balance_amount = balance_amount
        self.__increased_at = increased_at

    def create_event_name(self) -> str:
        return 'balance.increased'

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'increased_amount': self.__increased_amount,
            'balance_amount': self.__balance_amount,
            'balance_id': str(self.get_entity()),
            'increased_at': self.__increased_at
        }
