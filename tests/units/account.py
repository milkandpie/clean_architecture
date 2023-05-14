from datetime import datetime

import pytest

from src.applications import (
    AccountRegisteringService,
    AccountRegisterCommand,
    BalanceTopUpService,
    BalanceTopUpCommand)
from src.infrastructure import (
    InMemoryAccountRegisteringRepository,
    InMemorySession, InMemoryBalanceTopUpRepository)


@pytest.mark.asyncio
async def test_create_account():
    db = {}
    session = InMemorySession(db)
    repository = InMemoryAccountRegisteringRepository(session)
    command_handler = AccountRegisteringService(repository)
    command = AccountRegisterCommand('Oberyn Nymeros Martell',
                                     'lord_viper@mail.com',
                                     datetime.utcnow())

    await command_handler.handle(command)
    account = await repository.create(command)
    assert account.get_email() == command.email


@pytest.mark.asyncio
async def test_top_up_created_account():
    db = {}
    session = InMemorySession(db)
    repository = InMemoryAccountRegisteringRepository(session)
    command_handler = AccountRegisteringService(repository)
    command = AccountRegisterCommand('Oberyn Nymeros Martell',
                                     'lord_viper@mail.com',
                                     datetime.utcnow())

    await command_handler.handle(command)

    top_up_repository = InMemoryBalanceTopUpRepository(session)
    top_up_command_handler = BalanceTopUpService(top_up_repository)

    top_up_command = BalanceTopUpCommand('lord_viper@mail.com',
                                         1000,
                                         'Test decreased',
                                         datetime.utcnow())
    await top_up_command_handler.handle(top_up_command)
    balance = await top_up_repository.create(top_up_command)

    assert balance.get_amount() == 1000
