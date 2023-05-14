from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementFile
from ._management_resource import (
    ManagementExtraIn)
from ._management_resource import (
    AdditionManagementResource)


class FileIn(ManagementExtraIn):
    file_type: str = None
    video_type: str = None
    object_type: str = None
    content_type: str = None

    url: str = None
    size: int = None

    locale: str = None
    ordered: int = None
    extra: dict = None


class FilePayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: FileIn | List[FileIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class FileIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: FileIn | List[FileIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class FileResource(AdditionManagementResource):
    def __init__(self):
        super(FileResource, self).__init__('/files')

    def create_document(self) -> Type[Document]:
        return ManagementFile

    async def post(self, request=Depends(FilePayloadRequest)):
        return await super(FileResource, self).post(request)

    async def patch(self, request=Depends(FileIdPayloadRequest)):
        return await super(FileResource, self).patch(request=request)
