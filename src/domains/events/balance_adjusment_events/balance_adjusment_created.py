from datetime import datetime

from src.domains.common import BaseEntityEvent
from dataclasses import dataclass
from src.domains.entities import BalanceAdjustment


@dataclass
class BalanceAdjustmentCreated(BaseEntityEvent):
    def __init__(self, email: str, executed_at: datetime, balance_adjustment: BalanceAdjustment):
        super().__init__(balance_adjustment)
        self.__email = email
        self.__executed_at = executed_at

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'email': self.__email,
            'executed_at': self.__executed_at
        }
