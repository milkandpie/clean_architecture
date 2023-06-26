from datetime import datetime

import pytest

from clean_architecture.domains import Balance, EntityId
from clean_architecture.applications import (
    BalanceDecreasingService,
    BalanceDecreasingCommand,
    BalanceTopUpService,
    BalanceTopUpCommand)
from clean_architecture.infrastructure import (
    InMemoryBalanceDecreasingRepository,
    InMemoryBalanceTopUpRepository,
    InMemoryDataBase,
    InMemorySession)


@pytest.mark.parametrize('balance, top_up_amounts, expected_amount', [
    (Balance(0, 0, EntityId()), [-10000, -20000, -3000], 33000),
    (Balance(10000, 0, EntityId()), [10000, 2000], -2000),
])
def test_multiple_charges(balance, top_up_amounts, expected_amount):
    for amount in top_up_amounts:
        balance.charge(amount)

    assert balance.get_amount() == expected_amount


@pytest.mark.asyncio
async def test_decreasing_failed():
    session = InMemorySession(InMemoryDataBase())
    repository = InMemoryBalanceDecreasingRepository(session)
    command_handler = BalanceDecreasingService(repository=repository)

    command = BalanceDecreasingCommand('lord_viper@mail.com',
                                       1000,
                                       'Test decreased',
                                       datetime.utcnow())

    await command_handler.handle(command)

    balance = await repository.create(command)

    assert balance.get_amount() == 0


@pytest.mark.asyncio
async def test_decreasing():
    session = InMemorySession(InMemoryDataBase(**{'balance:lord_viper@mail.com': 15000}))
    repository = InMemoryBalanceDecreasingRepository(session)
    command_handler = BalanceDecreasingService(repository=repository)

    command = BalanceDecreasingCommand('lord_viper@mail.com',
                                       1000,
                                       'Test decreased',
                                       datetime.utcnow())

    await command_handler.handle(command)
    balance = await repository.create(command)
    assert balance.get_amount() == 14000


@pytest.mark.asyncio
async def test_increasing():
    session = InMemorySession(InMemoryDataBase())
    repository = InMemoryBalanceTopUpRepository(session)
    command_handler = BalanceTopUpService(repository=repository)

    command = BalanceTopUpCommand('lord_viper@mail.com',
                                  1000,
                                  'Test top up',
                                  datetime.utcnow())
    await command_handler.handle(command)
    balance = await repository.create(command)

    assert balance.get_amount() == 1000
