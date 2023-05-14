from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementNotable
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class NotableIn(ManagementIn):
    type: str = 'notable'


class NotablePayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: NotableIn | List[NotableIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class NotableIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: NotableIn | List[NotableIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class NotableResource(ManagementResource):
    def __init__(self):
        super(NotableResource, self).__init__('/notables')

    def create_document(self) -> Type[Document]:
        return ManagementNotable

    async def post(self, request=Depends(NotablePayloadRequest)):
        return await super(NotableResource, self).post(request)

    async def patch(self,
                    request=Depends(NotableIdPayloadRequest)):
        return await super(NotableResource, self).patch(request)
