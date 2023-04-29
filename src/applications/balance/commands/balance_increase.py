from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import (
    Balance,
    BalanceIncreased)


@dataclass()
class BalanceIncreasingCommand(Command):
    email: str
    amount: int
    comment: str
    executed_at: datetime

    # TODO: Validate command


class BalanceIncreasingRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceIncreasingCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance):
        pass


class BalanceIncreasingService(CommandHandleable):
    def __init__(self, repository: BalanceIncreasingRepository):
        self.__repository = repository

    async def handle(self, command: BalanceIncreasingCommand):
        balance = await self.__repository.create(command)
        amount_before_increasing = balance.get_amount()

        balance.charge(-abs(command.amount),
                       comment=command.comment)

        balance.add_event(BalanceIncreased(amount_before_increasing, command.amount, command.executed_at, balance))
        return await self.__repository.save(balance)
