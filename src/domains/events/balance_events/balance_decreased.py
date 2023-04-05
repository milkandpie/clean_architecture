from datetime import datetime

from src.domains.common import BaseEntityEvent
from dataclasses import dataclass
from src.domains.entities import Balance


@dataclass
class BalanceDecreased(BaseEntityEvent):
    def __init__(self, email: str, decreased_at: datetime, balance: Balance):
        super().__init__(balance)
        self.__email = email
        self.__decreased_at = decreased_at

    def to_dict(self) -> dict:
        result = super().to_dict()
        return {
            **result,
            'email': self.__email,
            'decreased_at': self.__decreased_at
        }
