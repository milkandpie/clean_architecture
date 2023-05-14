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
from models.auth import Organization
from services import (
    AsyncModelUpdatable,
    AsyncModelCreatable,
    OrganizationUpdatableService,
    OrganizationCreatableService)
from ._auth_resource import AuthResource


class OrganizationIn(BaseModel):
    code: str
    summary: str
    priority: int

    address: Optional[str] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None


class OrganizationPayloadRequest(AdminPayloadRequest):
    def __init__(self, payload: OrganizationIn | List[OrganizationIn],
                 requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(payload, requested)


class OrganizationIdPayloadRequest(AdminIdPayloadRequest):
    def __init__(self, payload: OrganizationIn | List[OrganizationIn],
                 requested: AdminIdRequest = Depends(AdminIdRequest)):
        super().__init__(payload, requested)


class OrganizationResource(AuthResource):
    def create_document(self) -> Type[Document]:
        return Organization

    def _create_creatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelCreatable:
        return OrganizationCreatableService(session=session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        return OrganizationUpdatableService(session=session)

    async def post(self, request=Depends(OrganizationPayloadRequest)):
        return await super(OrganizationResource, self).post(request)

    async def patch(self, request=Depends(OrganizationIdPayloadRequest)):
        return await super(OrganizationResource, self).patch(request)
