from src.applications import (
    BasedRepositoryInjector,
    AccountRegisteringRepository,
    AccountLoginRepository,
    BalanceDecreasingRepository,
    BalanceTopUpRepository,
    PasswordEncoded,
    TokenEncoded)
from .repositories import (
    InMemoryAccountRegisteringRepository,
    InMemoryAccountLoggingInRepository,
    InMemoryBalanceDecreasingRepository,
    InMemoryBalanceTopUpRepository)
from src.infrastructure.common import (
    JWTTokenEncoder,
    MD5PasswordEncoder)
from .session import (
    InMemorySession,
    InMemoryDataBase)

in_memory_injector = BasedRepositoryInjector(
    {
        InMemoryDataBase: {},
        InMemorySession: InMemorySession,
        AccountRegisteringRepository: InMemoryAccountRegisteringRepository,
        BalanceDecreasingRepository: InMemoryBalanceDecreasingRepository,
        AccountLoginRepository: InMemoryAccountLoggingInRepository,
        BalanceTopUpRepository: InMemoryBalanceTopUpRepository,
        PasswordEncoded: MD5PasswordEncoder,
        TokenEncoded: JWTTokenEncoder

    }
)
