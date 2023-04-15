from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import (
    Balance,
    BalanceDecreased,
    BalanceDecreasedFailed,
    BalanceInsufficientException)


@dataclass()
class BalanceChargedCommand(Command):
    email: str
    amount: float
    executed_at: datetime


class BalanceChargeableService(CommandHandleable):
    def __init__(self, charged_amount: float, current_amount: float, email: str,
                 executed_at: datetime = None):
        self.__email = email
        self.__executed_at = executed_at
        self.__charged_amount = charged_amount

        self.__balance = Balance(current_amount)

    def handle(self) -> Balance:
        try:
            self.__balance.decrease(self.__charged_amount)

            self.__balance.add_event(BalanceDecreased(self.__email, self.__executed_at, self.__balance))
        except BalanceInsufficientException:
            self.__balance.add_event(BalanceDecreasedFailed(self.__email, self.__executed_at, self.__balance))

        return self.__balance


class ChargedRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceChargedCommand) -> BalanceChargedCommandHandler:
        pass

    @abstractmethod
    async def save(self, balance: BalanceChargedCommandHandler):
        pass
