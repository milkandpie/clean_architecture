from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementCategory
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class CategoryIn(ManagementIn):
    type: str = 'category'


class CategoryPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: CategoryIn | List[CategoryIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class CategoryIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: CategoryIn | List[CategoryIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class CategoryResource(ManagementResource):
    def __init__(self):
        super(CategoryResource, self).__init__('/categories')

    def create_document(self) -> Type[Document]:
        return ManagementCategory

    async def post(self, request=Depends(CategoryPayloadRequest)):
        return await super(CategoryResource, self).post(request)

    async def patch(self, request=Depends(CategoryIdPayloadRequest)):
        return await super(CategoryResource, self).patch(request)
