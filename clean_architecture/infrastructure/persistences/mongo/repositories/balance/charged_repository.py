from clean_architecture.applications import BalanceDecreasingRepository, BalanceDecreasingCommand
from clean_architecture.domains import Balance


class MongoDecreasingRepository(BalanceDecreasingRepository):

    async def create(self, command: BalanceDecreasingCommand) -> Balance:
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
