from clean_architecture.applications import (
    MediatorGetter,
    AccountLoginCommand,
    AccountLoginRepository)
from clean_architecture.domains import Account, EntityId
from clean_architecture.infrastructure.persistences.in_memory.common import InMemoryRepositoryInjector
from ...session import InMemorySession


class InMemoryAccountLoggingInRepository(AccountLoginRepository):
    def __init__(self, session: InMemorySession):
        self.__session = session

    async def create(self, command: AccountLoginCommand) -> Account:
        current_name = self.__session.get(f'account:{command.username}')
        encoded_password = self.__session.get(f'password:{command.username}')
        if current_name is None:
            return Account('', '',
                           encoded_password=encoded_password,
                           _id=EntityId(command.username))

        return Account(command.username, current_name,
                       encoded_password=encoded_password,
                       _id=EntityId(command.username))

    async def save(self, account: Account):
        mediator = MediatorGetter.get_mediator('event', injector=InMemoryRepositoryInjector())

        for event in account.get_events():
            await mediator.handle(event)

        self.__session.add_delayed_events([event.to_dict() for event in account.get_delayed_events()])
        self.__session.add_integrate_events([event.to_dict() for event in account.get_integration_events()])

        return account
