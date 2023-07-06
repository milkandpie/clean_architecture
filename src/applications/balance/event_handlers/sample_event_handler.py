from src.applications.common import EventHandleable
from src.domains import BalanceIncreased


class ToAnotherAggregateHandler(EventHandleable):
    async def handle(self, event: BalanceIncreased):
        print(f'\nYour balance increase {event.increased_amount}. '
              f'Current balance amount is {event.balance_amount + event.increased_amount}')
