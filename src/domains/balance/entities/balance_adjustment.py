from dataclasses import dataclass

from src.domains.common import (
    Entity,
    EntityId)


@dataclass
class BalanceAdjustment(Entity):
    number: int
    comment: str
    amount: float
    balance_id: EntityId
    adjustment_type: str
    balance_amount: float
