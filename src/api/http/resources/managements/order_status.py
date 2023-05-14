from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthIdRequest,
    UserAuthRequest)
from models.management import ManagementOrderStatus
from ._management_resource import (
    AdditionManagementResource,
    ManagementExtraIn)


class OrderStatusIn(ManagementExtraIn):
    organization_id: str
    status: str


class OrderStatusPayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: OrderStatusIn | List[OrderStatusIn],
                 requested=Depends(UserAuthRequest)):
        super().__init__(payload, requested)


class OrderStatusIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: OrderStatusIn | List[OrderStatusIn],
                 requested=Depends(AuthIdRequest)):
        super().__init__(payload, requested)


class OrderStatusResource(AdditionManagementResource):
    def __init__(self):
        super(OrderStatusResource, self).__init__('/order_statuses')

    def create_document(self) -> Type[Document]:
        return ManagementOrderStatus

    async def post(self, request=Depends(OrderStatusPayloadRequest)):
        return await super(OrderStatusResource, self).post(request)

    async def patch(self, request=Depends(OrderStatusIdPayloadRequest)):
        return await super(OrderStatusResource, self).patch(request)
