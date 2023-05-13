from src.applications import (
    based_mediator,
    BalanceDecreasingRepository,
    BalanceDecreasingCommand)
from src.domains import Balance, EntityId

from ...session import InMemorySession


class InMemoryBalanceDecreasingRepository(BalanceDecreasingRepository):
    def __init__(self, session: InMemorySession):
        self.__session = session

    async def create(self, command: BalanceDecreasingCommand) -> Balance:
        current_amount = self.__session.get(f'balance:{command.email}')
        if current_amount is None:
            return Balance(0, 0, EntityId(command.email))

        current_ba_number = self.__session.get(f'balance_adjustment:{command.email}:balance_adjustment_count') or 0
        return Balance(current_amount, current_ba_number, EntityId(command.email))

    async def rollback(self, balance: Balance) -> Balance:
        events = [event.to_dict() for event in balance.get_events()]
        self.__session.add_events(events)
        return balance

    async def save(self, balance: Balance):
        balance_account_id = balance.get_account_id()
        amount = balance.get_amount()
        self.__session.set(f'balance:{balance_account_id}', amount)
        self.__session.set(f'balance_adjustment:{balance_account_id}:balance_adjustment_count',
                           balance.get_balance_adjustment_number())

        balance_adjustments = balance.get_balance_adjustments()
        for balance_adjustment in balance_adjustments:
            ba_number = balance_adjustment.get_number()
            self.__session.set(f'balance_adjustment:{balance_account_id}:{ba_number}', balance_adjustment.to_dict())

        for event in balance.get_events():
            based_mediator.handle(event)

        self.__session.add_delayed_events([event.to_dict() for event in balance.get_delayed_events()])
        self.__session.add_integrate_events([event.to_dict() for event in balance.get_integration_events()])

        return balance
