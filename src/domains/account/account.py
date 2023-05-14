from datetime import datetime

from src.domains.common import AggregateRoot, EntityId, EventId
from .events import AccountRegistered
from .exceptions import AccountRegisterException


class Account(AggregateRoot):
    def __init__(self, email: str, name: str, _id: EntityId = None):
        super().__init__()
        self.__name = name
        self.__email = email

    def register(self, email: str, name: str, register_at: datetime):
        if self.__email == email:
            raise AccountRegisterException(f'Email taken: {email}')
        new_account = Account(email, name)
        event = AccountRegistered(EventId(), new_account.__class__.__name__, new_account.get_id(),
                                  registered_at=register_at,
                                  email=email,
                                  name=name)
        new_account.add_event(event)
        new_account.add_integration_event(event.to_integration('billing.account_registered'))

        return new_account

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email
