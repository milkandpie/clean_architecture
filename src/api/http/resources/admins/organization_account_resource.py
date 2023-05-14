from typing import Type, List

from beanie import Document
from fastapi import Depends
from pydantic import BaseModel
from pymongo.client_session import ClientSession

from apps.http.requests import (
    AdminIdRequest,
    AdminAuthRequest,
    AdminPayloadRequest,
    AdminIdPayloadRequest)
from models.auth import OrganizationAccount
from services import (
    AsyncModelCreatable,
    AsyncModelUpdatable,
    OrganizationAccountCreatableService,
    OrganizationAccountUpdatableService)
from ._auth_resource import AuthResource


class OrganizationAccountIn(BaseModel):
    account_id: str
    organization_id: str

    role_ids: List[str]


class OrganizationAccountPayloadRequest(AdminPayloadRequest):
    def __init__(self, payload: OrganizationAccountIn | List[OrganizationAccountIn],
                 requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(payload, requested)


class OrganizationAccountIdPayloadRequest(AdminIdPayloadRequest):
    def __init__(self, payload: OrganizationAccountIn | List[OrganizationAccountIn],
                 requested: AdminIdRequest = Depends(AdminIdRequest)):
        super().__init__(payload, requested)


class OrganizationAccountResource(AuthResource):
    def __init__(self):
        super(OrganizationAccountResource, self).__init__(path='/organization/accounts')

    def create_document(self) -> Type[Document]:
        return OrganizationAccount

    def _create_creatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelCreatable:
        return OrganizationAccountCreatableService(session=session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        return OrganizationAccountUpdatableService(session=session)

    async def post(self, request=Depends(OrganizationAccountPayloadRequest)):
        return await super(OrganizationAccountResource, self).post(request=request)

    async def patch(self, request=Depends(OrganizationAccountIdPayloadRequest)):
        return await super(OrganizationAccountResource, self).patch(request=request)
