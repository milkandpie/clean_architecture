from datetime import datetime
from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthIdRequest,
    UserAuthRequest)
from models.management import ManagementStorageOrigin
from ._management_resource import (
    ManagementExtraIn,
    AdditionManagementResource)


class StorageOrigin(ManagementExtraIn):
    place: str = None

    transfer_name: str = None
    transfer_block: str = None
    transfer_ward: str = None
    transfer_district: str = None
    transfer_province: str = None

    collector_name: str = None
    collector_block: str = None
    collector_ward: str = None
    collector_district: str = None
    collector_province: str = None

    manufacture_name: str = None
    manufacture_note: str = None
    manufacture_time: datetime = None
    manufacture_place: str = None
    manufacture_technique: str = None


class StorageOriginPayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: StorageOrigin | List[StorageOrigin],
                 requested=Depends(UserAuthRequest)):
        super().__init__(payload, requested)


class StorageOriginIDPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: StorageOrigin | List[StorageOrigin],
                 requested=Depends(AuthIdRequest)):
        super().__init__(payload, requested)


class StorageOriginResource(AdditionManagementResource):
    def __init__(self):
        super(StorageOriginResource, self).__init__('/storage_origins')

    def create_document(self) -> Type[Document]:
        return ManagementStorageOrigin

    async def post(self, request=Depends(StorageOriginPayloadRequest)):
        return await super(StorageOriginResource, self).post(request)

    async def patch(self, request=Depends(StorageOriginIDPayloadRequest)):
        return await super(StorageOriginResource, self).patch(request)
