from datetime import datetime
from typing import Type, List, Optional

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from fastapi import Depends
from pydantic import (
    BaseModel,
    Field)
from pymongo.client_session import ClientSession

from apps.http.requests import (
    AdminIdRequest,
    AdminAuthRequest,
    AdminPayloadRequest,
    AdminIdPayloadRequest)
from models.auth import Account
from services import (
    AccountCreatableService,
    AccountDeletableService,
    AccountUpdatableService,
    AsyncModelCreatable,
    AsyncModelDeletable,
    AsyncModelUpdatable)
from ._auth_resource import AuthResource


class AccountIn(BaseModel):
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password: str
    email: str
    phone: str


class AccountUpdate(BaseModel):
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password: Optional[str]
    phone: Optional[str]


class AccountOut(BaseModel):
    # Filter password on out
    id: Optional[PydanticObjectId] = Field(alias='_id')
    created: datetime
    updated: datetime

    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: str
    phone: str


class AccountPayloadRequest(AdminPayloadRequest):
    def __init__(self, payload: AccountIn | List[AccountIn],
                 requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(payload, requested)


class AccountIdPayloadRequest(AdminIdPayloadRequest):
    def __init__(self, payload: AccountUpdate | List[AccountUpdate],
                 requested: AdminIdRequest = Depends(AdminIdRequest)):
        super().__init__(payload, requested)


class AccountResource(AuthResource):
    def create_document(self) -> Type[Document]:
        return Account

    def create_project_document(self) -> Type[BaseModel] | None:
        return AccountOut

    def _create_creatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelCreatable:
        return AccountCreatableService(session=session)

    def _create_deletable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelDeletable:
        return AccountDeletableService(session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        return AccountUpdatableService(session)

    async def post(self, request=Depends(AccountPayloadRequest)):
        return await super(AccountResource, self).post(request)

    async def patch(self, request=Depends(AccountIdPayloadRequest)):
        return await super(AccountResource, self).patch(request)
