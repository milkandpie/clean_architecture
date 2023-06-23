from pydantic import BaseModel


class ResourceItem(BaseModel):
    category_code: str
    resource_name: str
    resource_ref: str
    region_name: str
    related_ref: str
    quantity: float
    plan_name: str
