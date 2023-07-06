from src.domains import AccountRegistered, Balance
from src.applications.common import EventRepository, EventHandleable


class AccountBalanceCreateRepository(EventRepository):
    async def create(self, event: AccountRegistered) -> Balance:
        pass

    async def save(self, domain: Balance) -> Balance:
        pass


class AccountBalanceCreateHandler(EventHandleable):
    def __init__(self, repository: AccountBalanceCreateRepository):
        self.__repository = repository

    async def handle(self, event: AccountRegistered):
        balance = await self.__repository.create(event)
        balance.create(event.aggregate_id)
        return await self.__repository.save(balance)
