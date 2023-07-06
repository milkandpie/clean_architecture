from datetime import datetime

from src.domains.common import AggregateRoot, EntityId, EventId
from .events import (
    AccountRegistered,
    AccountFailedLoggedIn,
    AccountLoggedIn)
from .exceptions import (
    AccountRegisterException,
    AccountLoginException)


class Account(AggregateRoot):
    def __init__(self, email: str, name: str,
                 encoded_password: str = None,
                 _id: EntityId = None):
        super().__init__()
        self.__name = name
        self.__email = email
        self.__encoded_password = encoded_password

    def register(self, email: str, name: str, encoded_password: str, register_at: datetime) -> 'Account':
        if self.__email == email:
            raise AccountRegisterException(f'Email taken: {email}')

        new_account = Account(email, name, encoded_password=encoded_password)
        event = AccountRegistered(EventId(), new_account.__class__.__name__, new_account.get_id(),
                                  registered_at=register_at,
                                  email=email,
                                  name=name)
        new_account.add_event(event)
        new_account.add_integration_event(event.to_integration('billing.account_registered'))

        return new_account

    def login(self, encoded_password: str, logged_at: datetime) -> 'Account':
        if not self.__email:
            self.add_integration_event(AccountFailedLoggedIn(EventId(), self.__class__.__name__, self.get_id(),
                                                             email=self.__email,
                                                             reason='Invalid email',
                                                             logged_in_at=logged_at)
                                       .to_integration('billing.invalid_account_logged_in'))
            raise AccountLoginException('')

        elif self.__encoded_password != encoded_password:
            self.add_integration_event(AccountFailedLoggedIn(EventId(), self.__class__.__name__, self.get_id(),
                                                             email=self.__email,
                                                             reason='Invalid email',
                                                             logged_in_at=logged_at)
                                       .to_integration('billing.invalid_password_logged_in'))

        else:
            self.add_integration_event(AccountLoggedIn(EventId(), self.__class__.__name__, self.get_id(),
                                                       email=self.__email,
                                                       logged_in_at=logged_at)
                                       .to_integration('billing.account_logged_in'))

        return self

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email

    def get_encoded_password(self) -> str:
        return self.__encoded_password

