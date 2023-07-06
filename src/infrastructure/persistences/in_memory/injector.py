from src.applications import (
    BasedRepositoryInjector,
    AccountRegisteringRepository,
    AccountLoginRepository,
    BalanceDecreasingRepository,
    BalanceTopUpRepository,
    PasswordEncoded,
    TokenUtils)
from src.infrastructure.common import (
    JWTTokenEncoder,
    MD5PasswordEncoder)
from .repositories import (
    InMemoryAccountRegisteringRepository,
    InMemoryAccountLoggingInRepository,
    InMemoryBalanceDecreasingRepository,
    InMemoryBalanceTopUpRepository)
from .session import (
    InMemorySession,
    InMemoryDataBase)

database = InMemoryDataBase()


class InMemoryInjector(BasedRepositoryInjector):
    def __init__(self):
        super().__init__({
            InMemoryDataBase: database,
            InMemorySession: InMemorySession,
            BasedRepositoryInjector: InMemoryInjector,
            AccountRegisteringRepository: InMemoryAccountRegisteringRepository,
            BalanceDecreasingRepository: InMemoryBalanceDecreasingRepository,
            AccountLoginRepository: InMemoryAccountLoggingInRepository,
            BalanceTopUpRepository: InMemoryBalanceTopUpRepository,
            PasswordEncoded: MD5PasswordEncoder,
            TokenUtils: JWTTokenEncoder

        })
