from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementTag
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class TagIn(ManagementIn):
    type: str = 'tag'


class TagPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: TagIn | List[TagIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class TagIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: TagIn | List[TagIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class TagResource(ManagementResource):
    def __init__(self):
        super(TagResource, self).__init__('tags')

    def create_document(self) -> Type[Document]:
        return ManagementTag

    async def post(self, request=Depends(TagPayloadRequest)):
        return await super(TagResource, self).post(request)

    async def patch(self, request=Depends(TagIdPayloadRequest)):
        return await super(TagResource, self).patch(request)
