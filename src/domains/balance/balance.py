from datetime import datetime
from typing import List

from src.domains.common import AggregateRoot, EntityId
from .constants import DECREASED, INCREASED
from .entities import BalanceAdjustment
from .events import (
    BalanceIncreased,
    BalanceDecreased,
    BalanceDecreasedFailed)


class Balance(AggregateRoot):
    def __init__(self, amount: int, balance_adjustment_number: int, account_id: EntityId,
                 _id: EntityId = None):
        super().__init__(_id)
        self.__amount: int = amount
        self.__account_id: EntityId = account_id
        self.__balance_adjustment_number: int = balance_adjustment_number

        self.__balance_adjustments: List[BalanceAdjustment] = []

    def top_up(self, top_up_amount: int,
               comment: str = None,
               executed_at: datetime = None) -> bool:
        before_top_up_amount = self.__amount

        self.charge(-abs(top_up_amount), comment=comment)
        self.add_event(BalanceIncreased(before_top_up_amount, top_up_amount, executed_at, self.get_id()))
        return True

    def decrease(self, decreasing_amount: int,
                 comment: str = None,
                 executed_at: datetime = None) -> bool:
        amount_before_decreasing = self.__amount
        if amount_before_decreasing < decreasing_amount:
            self.add_event(BalanceDecreasedFailed(amount_before_decreasing, decreasing_amount, executed_at,
                                                  self.get_id()))
            return False

        self.charge(decreasing_amount, comment=comment)
        self.add_event(BalanceDecreased(amount_before_decreasing, decreasing_amount, executed_at, self.get_id()))
        return True

    def charge(self, charging_amount: int,
               comment: str = None) -> int:
        self.__balance_adjustment_number += 1
        current_amount = self.__amount
        self.__amount -= charging_amount

        adjustment_type = INCREASED if current_amount <= self.__amount else DECREASED
        balance_adjustment = BalanceAdjustment(self.__balance_adjustment_number, comment, abs(charging_amount),
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
