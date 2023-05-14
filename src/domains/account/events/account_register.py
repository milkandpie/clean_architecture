from dataclasses import dataclass
from datetime import datetime

from src.domains.common import DomainEvent


@dataclass
class AccountRegistered(DomainEvent):
    name: str
    email: str
    registered_at: datetime
