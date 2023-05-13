from src.applications import (
    BalanceTopUpRepository,
    BalanceTopUpCommand,
    based_mediator)
from src.domains import Balance, EntityId
from src.infrastructure.persistences.in_memory.session import InMemorySession


class InMemoryBalanceTopUpRepository(BalanceTopUpRepository):
    def __init__(self, session: InMemorySession):
        self.__session = session

    async def create(self, command: BalanceTopUpCommand) -> Balance:
        current_amount = self.__session.get(f'balance:{command.email}')
        if current_amount is None:
            return Balance(0, 0, EntityId(command.email))

        current_ba_number = self.__session.get(f'balance_adjustment:{command.email}:balance_adjustment_count')
        return Balance(current_amount, current_ba_number, EntityId(command.email))

    async def save(self, balance: Balance):
        balance_account_id = balance.get_account_id()
        self.__session.set(f'balance:{balance_account_id}', balance.get_amount())
        self.__session.set(f'balance_adjustment:{balance_account_id}:balance_adjustment_count',
                           balance.get_balance_adjustment_number())

        balance_adjustments = balance.get_balance_adjustments()
        for balance_adjustment in balance_adjustments:
            self.__session.set(f'balance_adjustment:{balance.get_account_id()}:{balance_adjustment.get_number()}',
                               balance_adjustment.to_dict())

        for event in balance.get_events():
            based_mediator.handle(event)

        self.__session.add_delayed_events([event.to_dict() for event in balance.get_delayed_events()])
        self.__session.add_integrate_events([event.to_dict() for event in balance.get_integration_events()])

        return balance
