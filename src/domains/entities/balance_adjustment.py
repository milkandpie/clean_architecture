from dataclasses import dataclass

from src.domains.common import BasedEntity


@dataclass
class BalanceAdjustment(BasedEntity):
    number: int
    comment: str
    amount: float
    balance_id: str
    adjustment_type: str
    balance_amount: float
