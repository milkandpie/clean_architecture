from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementDocument
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class DocumentIn(ManagementIn):
    type: str = 'document'


class DocumentPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: DocumentIn | List[DocumentIn],
                 requested: ManagementRequest = Depends(ManagementRequest)):
        super().__init__(payload, requested)


class DocumentIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: DocumentIn | List[DocumentIn],
                 requested: ManagementIdRequest = Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class DocumentResource(ManagementResource):
    def __init__(self):
        super(DocumentResource, self).__init__('/documents')

    def create_document(self) -> Type[Document]:
        return ManagementDocument

    async def post(self, request=Depends(DocumentPayloadRequest)):
        return await super(DocumentResource, self).post(request)

    async def patch(self, request=Depends(DocumentIdPayloadRequest)):
        return await super(DocumentResource, self).patch(request)
