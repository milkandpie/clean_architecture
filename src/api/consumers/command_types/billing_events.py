from datetime import datetime

from src.applications import CouponApplyCommand

from pydantic import BaseModel


class PydanticCouponApplyCommand(BaseModel):
    usage_id: str
    bill_line: str
    billed_at: datetime

    def dict(self, *args, **kwargs):
        return {'billed_at': self.billed_at,
                'billing_id': self.bill_line,
                'resource_item_id': self.usage_id}


EVENTS = {
    'billing.resource_subscribed_billed': {'command_type': CouponApplyCommand,
                                           'based_model_type': PydanticCouponApplyCommand}
}
