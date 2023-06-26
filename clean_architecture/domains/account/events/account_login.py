from dataclasses import dataclass
from datetime import datetime

from clean_architecture.domains.common import DomainEvent


@dataclass
class AccountLoggedIn(DomainEvent):
    email: str
    logged_in_at: datetime


@dataclass
class AccountFailedLoggedIn(DomainEvent):
    email: str
    reason: str
    logged_in_at: datetime
