from src.applications import (
    BasedRepositoryInjector,
    AccountRegisteringRepository,
    AccountLoginRepository,
    BalanceDecreasingRepository,
    BalanceTopUpRepository,
    PasswordEncoded,
    TokenUtils)
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
        InMemoryDataBase: InMemoryDataBase(),
        InMemorySession: InMemorySession,
        AccountRegisteringRepository: InMemoryAccountRegisteringRepository,
        BalanceDecreasingRepository: InMemoryBalanceDecreasingRepository,
        AccountLoginRepository: InMemoryAccountLoggingInRepository,
        BalanceTopUpRepository: InMemoryBalanceTopUpRepository,
        PasswordEncoded: MD5PasswordEncoder,
        TokenUtils: JWTTokenEncoder

    }
)
