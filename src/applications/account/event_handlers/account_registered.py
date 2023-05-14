from src.domains import AccountRegistered, Balance
from src.applications.common import EventRepository, EventHandleable


class AccountBalanceCreateRepository(EventRepository):
    async def create(self, event: AccountRegistered) -> Balance:
        pass

    async def save(self, domain: Balance) -> Balance:
        pass


class AccountBalanceCreateHandler(EventHandleable):
    async def handle(self, event: AccountRegistered):
        repository = self._injector.get_concreate(AccountBalanceCreateRepository)
        balance = await repository.create(event)
        balance.create(event.aggregate_id)
        return await repository.save(balance)
