from dataclasses import dataclass

from src.domains.common import (
    Entity,
    EntityId)


class BalanceAdjustment(Entity):
    def __init__(self, number: int, comment: str, amount: int,
                 balance_id: EntityId, adjustment_type: str,
                 balance_amount: int,
                 _id: EntityId = None):
        super().__init__(_id)
        self.__amount: int = amount
        self.__number: int = number
        self.__comment: str = comment
        self.__balance_id: EntityId = balance_id
        self.__balance_amount: int = balance_amount
        self.__adjustment_type: str = adjustment_type

    def get_number(self) -> int:
        return self.__number
