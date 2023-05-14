from typing import Type, Optional, List

from beanie import Document
from fastapi import Depends
from pydantic import BaseModel
from pymongo.client_session import ClientSession

from apps.http.requests import (
    AdminIdRequest,
    AdminAuthRequest,
    AdminPayloadRequest,
    AdminIdPayloadRequest)
from models.auth import Role
from services import (
    AsyncModelCreatable,
    AsyncModelUpdatable,
    RoleCreatableService,
    RoleUpdatableService)
from ._auth_resource import AuthResource


class RoleIn(BaseModel):
    code: str
    summary: Optional[str]
    description: Optional[str]


class RolePayloadRequest(AdminPayloadRequest):
    def __init__(self, payload: RoleIn | List[RoleIn],
                 requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(payload, requested)


class RoleIDPayloadRequest(AdminIdPayloadRequest):
    def __init__(self, payload: RoleIn | List[RoleIn],
                 requested: AdminIdRequest = Depends(AdminIdRequest)):
        super().__init__(payload, requested)


class RoleResource(AuthResource):
    def create_document(self) -> Type[Document]:
        return Role

    def _create_creatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelCreatable:
        return RoleCreatableService(session=session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        return RoleUpdatableService(session=session)

    async def post(self, request=Depends(RolePayloadRequest)):
        return await super(RoleResource, self).post(request)

    async def patch(self, request=Depends(RoleIDPayloadRequest)):
        return await super(RoleResource, self).patch(request)
