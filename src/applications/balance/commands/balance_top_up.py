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
class BalanceTopUpCommand(Command):
    email: str
    amount: int
    comment: str
    executed_at: datetime

    # TODO: Validate command


class BalanceTopUpRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceTopUpCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance):
        pass


class BalanceTopUpService(CommandHandleable):
    def __init__(self, repository: BalanceTopUpRepository):
        self.__repository = repository

    async def handle(self, command: BalanceTopUpCommand):
        balance = await self.__repository.create(command)
        amount_before_increasing = balance.get_amount()
        balance.top_up(command.amount, comment=command.comment)

        balance.add_event(BalanceIncreased(amount_before_increasing, command.amount, command.executed_at, balance))
        await self.__repository.save(balance)
