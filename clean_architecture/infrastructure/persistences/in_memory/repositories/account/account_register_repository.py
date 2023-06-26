from clean_architecture.applications import (
    MediatorGetter,
    AccountRegisterCommand,
    BasedRepositoryInjector,
    AccountRegisteringRepository,
    AccountBalanceCreateRepository)
from clean_architecture.domains import Account, EntityId
from clean_architecture.infrastructure.persistences.in_memory.common import BalanceCreateRepository
from ...session import InMemorySession


class InMemoryAccountRegisteringRepository(AccountRegisteringRepository):
    def __init__(self, session: InMemorySession):
        self.__session = session

    async def create(self, command: AccountRegisterCommand) -> Account:
        current_name = self.__session.get(f'account:{command.email}')
        if current_name is None:
            return Account('', '', _id=EntityId(command.email))

        return Account(command.email, current_name, _id=EntityId(command.email))

    async def save(self, account: Account):
        self.__session.set(f'account:{account.get_email()}', account.get_name())
        self.__session.set(f'password:{account.get_email()}', account.get_encoded_password())

        mediator = (MediatorGetter.
                    get_mediator('event',
                                 injector=BasedRepositoryInjector({
                                     AccountBalanceCreateRepository: BalanceCreateRepository(self.__session)
                                 })))

        for event in account.get_events():
            await mediator.handle(event)

        self.__session.add_delayed_events([event.to_dict() for event in account.get_delayed_events()])
        self.__session.add_integrate_events([event.to_dict() for event in account.get_integration_events()])

        return account
