from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from clean_architecture.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from clean_architecture.domains import Balance


@dataclass
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
        super().__init__()
        self.__repository = repository

    async def handle(self, command: BalanceTopUpCommand):
        balance = await self.__repository.create(command)
        balance.top_up(command.amount,
                       comment=command.comment,
                       executed_at=command.executed_at)

        await self.__repository.save(balance)
