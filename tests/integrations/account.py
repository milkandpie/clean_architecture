from datetime import datetime

import pytest

from src.applications import (
    AccountRegisteringService,
    AccountRegisterCommand,
    AccountLoginCommand,
    AccountLoginService,
    BalanceTopUpService,
    BalanceTopUpCommand)
from src.infrastructure import (
    MD5PasswordEncoder, JWTTokenEncoder,
    InMemoryAccountLoggingInRepository,
    InMemoryAccountRegisteringRepository,
    InMemorySession, InMemoryDataBase, InMemoryBalanceTopUpRepository)


@pytest.mark.asyncio
async def test_create_account():
    session = InMemorySession(InMemoryDataBase())
    repository = InMemoryAccountRegisteringRepository(session)
    command_handler = AccountRegisteringService(repository=repository, password_encoded=MD5PasswordEncoder())
    command = AccountRegisterCommand('Oberyn Nymeros Martell',
                                     'lord_viper@mail.com',
                                     '12345',
                                     datetime.utcnow())

    await command_handler.handle(command)
    account = await repository.create(command)
    assert account.get_email() == command.email


@pytest.mark.asyncio
async def test_login():
    session = InMemorySession(InMemoryDataBase())
    repository = InMemoryAccountRegisteringRepository(session)
    command_handler = AccountRegisteringService(repository=repository, password_encoded=MD5PasswordEncoder())
    command = AccountRegisterCommand('Oberyn Nymeros Martell',
                                     'lord_viper@mail.com',
                                     '12345',
                                     datetime.utcnow())

    await command_handler.handle(command)

    login_command = AccountLoginCommand('lord_viper@mail.com',
                                        '12345',
                                        datetime.utcnow())
    login_repository = InMemoryAccountLoggingInRepository(session)
    command_handler = AccountLoginService(repository=login_repository, encoded=MD5PasswordEncoder(),
                                          token_utils=JWTTokenEncoder())
    await command_handler.handle(login_command)
    assert 1


@pytest.mark.asyncio
async def test_top_up_created_account():
    session = InMemorySession(InMemoryDataBase())
    repository = InMemoryAccountRegisteringRepository(session)
    command_handler = AccountRegisteringService(repository=repository, password_encoded=MD5PasswordEncoder())
    command = AccountRegisterCommand('Oberyn Nymeros Martell',
                                     'lord_viper@mail.com',
                                     '12345',
                                     datetime.utcnow())

    await command_handler.handle(command)

    top_up_repository = InMemoryBalanceTopUpRepository(session)
    top_up_command_handler = BalanceTopUpService(repository=top_up_repository)

    top_up_command = BalanceTopUpCommand('lord_viper@mail.com',
                                         1000,
                                         'Test decreased',
                                         datetime.utcnow())
    await top_up_command_handler.handle(top_up_command)
    balance = await top_up_repository.create(top_up_command)

    assert balance.get_amount() == 1000
