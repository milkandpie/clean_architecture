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
    BalanceDecreasedFailed)


@dataclass()
class BalanceDecreasingCommand(Command):
    email: str
    amount: int
    comment: str
    executed_at: datetime

    # TODO: Validate command


class BalanceDecreasingRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceDecreasingCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance) -> Balance:
        pass

    @abstractmethod
    async def rollback(self, balance: Balance) -> Balance:
        pass


class BalanceDecreasingService(CommandHandleable):
    def __init__(self, repository: BalanceDecreasingRepository):
        self.__repository = repository

    async def handle(self, command: BalanceDecreasingCommand) -> Balance:
        balance = await self.__repository.create(command)
        amount_before_decreasing = balance.get_amount()
        decreasing_amount = command.amount

        current_amount = balance.charge(decreasing_amount,
                                        comment=command.comment)

        if current_amount < 0:
            balance.add_event(
                BalanceDecreasedFailed(amount_before_decreasing, decreasing_amount, command.executed_at, balance))
            return await self.__repository.rollback(balance)

        else:
            balance.add_event(
                BalanceDecreased(amount_before_decreasing, decreasing_amount, command.executed_at, balance))

            return await self.__repository.save(balance)
