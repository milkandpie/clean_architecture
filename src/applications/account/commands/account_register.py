from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    CommandHandleable)
from src.domains import Account


@dataclass
class AccountRegisterCommand(Command):
    name: str
    email: str
    executed_at: datetime

    # TODO: Validate command


class AccountRegisteringRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: AccountRegisterCommand) -> Account:
        pass

    @abstractmethod
    async def save(self, account: Account) -> Account:
        pass


class AccountRegisteringService(CommandHandleable):
    def __init__(self, repository: AccountRegisteringRepository):
        super().__init__()
        self.__repository = repository

    async def handle(self, command: AccountRegisterCommand):
        account = await self.__repository.create(command)
        account = account.register(command.email, command.name, command.executed_at)
        await self.__repository.save(account)
