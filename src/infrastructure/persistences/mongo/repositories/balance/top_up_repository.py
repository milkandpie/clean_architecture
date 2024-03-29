from src.applications import BalanceTopUpRepository, BalanceTopUpCommand
from src.domains import Balance


class MongoBalanceTopUpRepository(BalanceTopUpRepository):
    async def create(self, command: BalanceTopUpCommand) -> Balance:
        # async query balance with command's email value
        return Balance(0)

    async def save(self, balance: Balance):
        # async start transaction
        document = balance.to_dict()
        # save document
        for event in balance.get_events():
            event_document = event.to_dict()
        # async commit transaction
        # Return some DTO
        return balance
