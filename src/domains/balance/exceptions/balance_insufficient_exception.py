from src.domains.common import DomainException


class BalanceInsufficientException(DomainException):
    def __init__(self, message: str = None):
        super().__init__(message or 'Insufficient balance')
