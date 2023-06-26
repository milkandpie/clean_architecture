from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from clean_architecture.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from clean_architecture.domains import Balance


@dataclass
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
        super().__init__()
        self.__repository = repository

    async def handle(self, command: BalanceDecreasingCommand):
        balance = await self.__repository.create(command)

        balance.decrease(command.amount,
                         comment=command.comment,
                         executed_at=command.executed_at)

        await self.__repository.save(balance)
