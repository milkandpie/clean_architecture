from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import Balance


@dataclass()
class BalanceChargedCommand(Command):
    email: str
    amount: int
    comment: str
    executed_at: datetime


class BalanceChargedRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceChargedCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance) -> Balance:
        pass

    @abstractmethod
    async def get_current_adjustment_number(self) -> int:
        pass


class BalanceChargeableService(CommandHandleable):
    def __init__(self, repository: BalanceChargedRepository):
        self.__repository = repository

    async def handle(self, command: BalanceChargedCommand):
        balance = await self.__repository.create(command)
        current_number = await self.__repository.get_current_adjustment_number()
        balance.increase(command.amount,
                         number=current_number,
                         comment=command.comment)

        return await self.__repository.save(balance)
