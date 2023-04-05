from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import Balance, BalanceIncreased


@dataclass()
class BalanceTopUpCommand(Command):
    email: str
    amount: float
    executed_at: datetime


class TopUpRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: BalanceTopUpCommand) -> Balance:
        pass

    @abstractmethod
    async def save(self, balance: Balance):
        pass


class BalanceTopUpCommandHandler(CommandHandleable):
    def __init__(self, repository: TopUpRepository):
        self.__repository = repository

    async def handle(self, command: BalanceTopUpCommand):
        balance = await self.__repository.create(command)
        # TODO: Balance adjustment
        balance.increase(command.amount)
        balance.add_event(BalanceIncreased(command.email, command.executed_at, balance))

        return self.__repository.save(balance)
