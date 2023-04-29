from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import Balance


@dataclass()
class BalanceTopUpCommand(Command):
    email: str
    amount: int
    comment: str
    executed_at: datetime


class TopUpRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceTopUpCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance):
        pass

    @abstractmethod
    async def get_current_adjustment_number(self) -> int:
        pass


class BalanceTopUpCommandHandler(CommandHandleable):
    def __init__(self, repository: TopUpRepository):
        self.__repository = repository

    async def handle(self, command: BalanceTopUpCommand):
        balance = await self.__repository.create(command)

        current_adjustment_number = await self.__repository.get_current_adjustment_number()
        balance.increase(command.amount,
                         number=current_adjustment_number,
                         comment=command.comment)

        return await self.__repository.save(balance)
