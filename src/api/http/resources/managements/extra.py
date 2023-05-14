from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementExtra
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class ExtraIn(ManagementIn):
    category_id: str
    type: str = 'extra'


class ExtraPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: ExtraIn | List[ExtraIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class ExtraIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: ExtraIn | List[ExtraIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class ExtraResource(ManagementResource):
    def __init__(self):
        super(ExtraResource, self).__init__('/extras')

    def create_document(self) -> Type[Document]:
        return ManagementExtra

    async def post(self, request=Depends(ExtraPayloadRequest)):
        return await super(ExtraResource, self).post(request)

    async def patch(self, request=Depends(ExtraIdPayloadRequest)):
        return await super(ExtraResource, self).patch(request)
