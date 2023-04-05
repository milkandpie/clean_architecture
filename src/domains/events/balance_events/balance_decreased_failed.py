from datetime import datetime

from src.domains.common import BaseEntityEvent
from dataclasses import dataclass
from src.domains.entities import Balance


@dataclass
class BalanceDecreasedFailed(BaseEntityEvent):
    def __init__(self, email: str, executed_at: datetime, balance: Balance):
        super().__init__(balance)
        self.__email = email
        self.__executed_at = executed_at

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'email': self.__email,
            'executed_at': self.__executed_at
        }
