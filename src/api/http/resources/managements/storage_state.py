from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthIdRequest,
    UserAuthRequest)
from models.management import ManagementStorageState
from ._management_resource import (
    ManagementExtraIn,
    AdditionManagementResource)


class StorageStateIn(ManagementExtraIn):
    place: str = None
    storage_state: str = None
    storage_order: str = None
    storage_record: str = None
    maintenance_state: str = None


class StorageStatePayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: StorageStateIn | List[StorageStateIn],
                 requested=Depends(UserAuthRequest)):
        super().__init__(payload, requested)


class StorageStateIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: StorageStateIn | List[StorageStateIn],
                 requested=Depends(AuthIdRequest)):
        super().__init__(payload, requested)


class StorageStateResource(AdditionManagementResource):
    def __init__(self):
        super(StorageStateResource, self).__init__('/storage_states')

    def create_document(self) -> Type[Document]:
        return ManagementStorageState

    async def post(self, request=Depends(StorageStatePayloadRequest)):
        return await super(StorageStateResource, self).post(request)

    async def patch(self, request=Depends(StorageStatePayloadRequest), ):
        return await super(StorageStateResource, self).patch(request)
