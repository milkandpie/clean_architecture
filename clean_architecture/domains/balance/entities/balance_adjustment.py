from dataclasses import dataclass

from clean_architecture.domains.common import (
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

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'amount': self.__amount,
            'number': self.__number,
            'comment': self.__comment,
            'balance_id': str(self.__balance_id),
            'balance_amount': self.__balance_amount,
            'adjustment_type': self.__adjustment_type
        }