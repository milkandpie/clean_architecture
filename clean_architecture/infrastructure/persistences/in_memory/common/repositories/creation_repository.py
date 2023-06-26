from clean_architecture.applications import (
    MediatorGetter,
    AccountBalanceCreateRepository)
from clean_architecture.domains import Balance, EntityId, AccountRegistered

from clean_architecture.infrastructure.persistences.in_memory.session import InMemorySession


class BalanceCreateRepository(AccountBalanceCreateRepository):
    def __init__(self, session: InMemorySession):
        self.__session = session

    async def create(self, event: AccountRegistered) -> Balance:
        current_amount = self.__session.get(f'balance:{event.email}')
        if current_amount is None:
            return Balance(0, 0, EntityId(event.email))

        current_ba_number = self.__session.get(f'balance_adjustment:{event.email}:balance_adjustment_count') or 0
        return Balance(current_amount, current_ba_number, EntityId(event.email))

    async def save(self, balance: Balance):
        balance_account_id = balance.get_account_id()
        amount = balance.get_amount()
        self.__session.set(f'balance:{balance_account_id}', amount)
        self.__session.set(f'balance_adjustment:{balance_account_id}:balance_adjustment_count',
                           balance.get_balance_adjustment_number())

        mediator = MediatorGetter.get_mediator('event')
        for event in balance.get_events():
            await mediator.handle(event)

        self.__session.add_delayed_events([event.to_dict() for event in balance.get_delayed_events()])
        self.__session.add_integrate_events([event.to_dict() for event in balance.get_integration_events()])

        return balance
