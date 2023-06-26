from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from clean_architecture.applications.common import (
    Command,
    Repository,
    PasswordEncoded,
    CommandHandleable)
from clean_architecture.domains import Account


@dataclass
class AccountRegisterCommand(Command):
    name: str
    email: str
    password: str
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
    def __init__(self, repository: AccountRegisteringRepository, password_encoded: PasswordEncoded):
        super().__init__()
        self.__repository = repository
        self.__encoded = password_encoded

    async def handle(self, command: AccountRegisterCommand):
        account = await self.__repository.create(command)
        account = account.register(command.email, command.name, self.__encoded.encode(command.password),
                                   command.executed_at)
        await self.__repository.save(account)
