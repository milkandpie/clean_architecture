from datetime import datetime

from src.domains.common import AggregateRoot


class Account(AggregateRoot):

    def register(self, email: str, name: str, phone: str, register_at: datetime):
        pass
