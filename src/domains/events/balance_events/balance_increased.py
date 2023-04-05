from datetime import datetime

from src.domains.common import BaseEntityEvent
from dataclasses import dataclass
from src.domains.entities import Balance


@dataclass
class BalanceIncreased(BaseEntityEvent):
    def __init__(self, email: str, increased_at: datetime, balance: Balance):
        super().__init__(balance)
        self.__email = email
        self.__increased_at = increased_at

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'email': self.__email,
            'increased_at': self.__increased_at
        }
