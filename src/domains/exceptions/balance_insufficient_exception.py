from ._domain_exception import DomainException


class BalanceInsufficientException(DomainException):
    def __init__(self, message: str = None):
        super().__init__(message or 'Insufficient balance')
