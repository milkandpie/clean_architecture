from typing import List

from src.domains.common import AggregateRoot, EntityId
from .constants import DECREASED, INCREASED
from .entities import BalanceAdjustment


class Balance(AggregateRoot):
    def __init__(self, amount: int, balance_adjustment_number: int, account_id: EntityId,
                 _id: EntityId = None):
        super().__init__(_id)
        self.__amount: int = amount
        self.__account_id: EntityId = account_id
        self.__balance_adjustment_number: int = balance_adjustment_number

        self.__balance_adjustments: List[BalanceAdjustment] = []

    def top_up(self, amount: int,
               comment: str = None) -> bool:
        self.charge(-abs(amount), comment=comment)
        return True

    def decrease(self, decreasing_amount: int,
                 comment: str = None) -> bool:
        amount_before_decreasing = self.__amount
        if amount_before_decreasing < decreasing_amount:
            return False

        self.charge(decreasing_amount, comment=comment)

        return True

    def charge(self, amount: int,
               comment: str = None) -> int:
        self.__balance_adjustment_number += 1
        current_amount = self.__amount
        self.__amount -= amount

        adjustment_type = INCREASED if current_amount <= self.__amount else DECREASED
        balance_adjustment = BalanceAdjustment(self.__balance_adjustment_number, comment, abs(amount),
                                               self.get_id(), adjustment_type,
                                               current_amount)
        self.__balance_adjustments.append(balance_adjustment)
        return self.__amount

    def get_amount(self) -> int:
        return self.__amount

    def get_balance_adjustments(self) -> List[BalanceAdjustment]:
        return self.__balance_adjustments

    def get_account_id(self) -> EntityId:
        return self.__account_id

    def get_balance_adjustment_number(self) -> int:
        return self.__balance_adjustment_number
