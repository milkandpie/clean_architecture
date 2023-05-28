from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.applications.common import (
    Command,
    Repository,
    PasswordEncoded,
    TokenUtils,
    EncodeData,
    CommandHandleable)
from src.domains import Account


@dataclass
class AccountLoginCommand(Command):
    username: str
    password: str
    executed_at: datetime
    # TODO: Validate command


class AccountLoginRepository(Repository, ABC):
    @abstractmethod
    async def create(self, command: AccountLoginCommand) -> Account:
        pass

    @abstractmethod
    async def save(self, account: Account) -> Account:
        pass


class AccountLoginService(CommandHandleable):
    def __init__(self, repository: AccountLoginRepository, encoded: PasswordEncoded, token_utils: TokenUtils):
        super().__init__()
        self.__encoded = encoded
        self.__repository = repository
        self.__token_utils = token_utils

    async def handle(self, command: AccountLoginCommand):
        account = await self.__repository.create(command)
        account = account.login(self.__encoded.encode(command.password), command.executed_at)
        await self.__repository.save(account)

        return self.__token_utils.encode(EncodeData(account.get_email()))
