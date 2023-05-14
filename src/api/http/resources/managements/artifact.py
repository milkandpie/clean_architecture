from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementArtifact
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class ArtifactIn(ManagementIn):
    type: str = 'artifact'


class ArtifactPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: ManagementIn | List[ManagementIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class ArtifactIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: ManagementIn | List[ManagementIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class ArtifactResource(ManagementResource):
    def __init__(self):
        super(ArtifactResource, self).__init__('/artifacts')

    def create_document(self) -> Type[Document]:
        return ManagementArtifact

    async def post(self, request=Depends(ArtifactPayloadRequest)):
        return await super(ArtifactResource, self).post(request)

    async def patch(self, request=Depends(ArtifactIdPayloadRequest)):
        return await super(ArtifactResource, self).patch(request)
