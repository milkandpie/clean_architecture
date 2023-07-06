from clean_architecture.applications import (
    BasedRepositoryInjector,
    PasswordEncoded,
    TokenUtils)
from clean_architecture.infrastructure.common import (
    JWTTokenEncoder,
    MD5PasswordEncoder)
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
            PasswordEncoded: MD5PasswordEncoder,
            TokenUtils: JWTTokenEncoder

        })