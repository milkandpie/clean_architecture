from src.domains import EventHandleable, BalanceIncreased


class ToAnotherAggregateHandler(EventHandleable):
    def handle(self, event: BalanceIncreased):
        print(f'\nYour balance increase {event.increased_amount}. '
              f'Current balance amount is {event.balance_amount + event.increased_amount}')
