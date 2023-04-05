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


class ChargedRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceChargedCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance):
        pass


class BalanceChargedCommandHandler(CommandHandleable):
    def __init__(self, repository: ChargedRepository):
        self.__repository = repository

    async def handle(self, command: BalanceChargedCommand):
        balance = await self.__repository.create(command)
        # TODO: Balance adjustment
        try:
            balance.decrease(command.amount)
            balance.add_event(BalanceDecreased(command.email, command.executed_at, balance))
        except BalanceInsufficientException:
            balance.add_event(BalanceDecreasedFailed(command.email, command.executed_at, balance))

        return self.__repository.save(balance)
