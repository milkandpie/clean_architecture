from abc import ABC
from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic import BaseModel
from pymongo.client_session import ClientSession

from apps.http.requests import (
    DeleteSchema,
    AuthURLParamsRequest,
    AuthIdPayloadRequest,
    ManagementIdRequest,
    ManagementParamsRequest,
    ManagementPayloadRequest,
    ManagementIdPayloadRequest)
from apps.http.resources.base_resource import BaseResource
from config import MANAGEMENT_MONGO_CONFIG
from services import (
    AuthenticationUser,
    AsyncModelCreatable,
    AsyncModelQueryable,
    AsyncModelDeletable,
    AsyncModelUpdatable,
    DocumentQueriedService,
    DocumentDeletableService,
    DocumentUpdatableService,
    DocumentCreatableService,
    DocumentLocaleCreatableService,
    DocumentLocaleUpdatableService,
    DocumentManagementCreatableService,
    DocumentManagementUpdatableService)


class ManagementIn(BaseModel):
    code: str = ''
    creator_id: str = ''
    register_at: datetime = None

    organization_id: str
    tag_ids: List[str] = []

    type: str
    status: str
    ordered: int
    avatar_url: str
    extra: dict = {}

    # Translation
    locale: str = str
    name: str = ''
    summary: str = ''
    description: str = ''
    translation_extra: str = ''


class ManagementExtraIn(BaseModel):
    based_type: str
    based_id: str
    organization_id: str


class DeleteIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: DeleteSchema | List[DeleteSchema],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class ManagementResource(BaseResource, ABC):
    def __init__(self, path: str = None):
        super(ManagementResource, self).__init__(path=path, mongo_config=MANAGEMENT_MONGO_CONFIG)

    async def get(self, request=Depends(ManagementParamsRequest)):
        return await super().get(request)

    async def delete(self, request=Depends(DeleteIdPayloadRequest)):
        return await super().delete(request)

    def _create_queryable(self, session: ClientSession | None = None,
                          request: ManagementPayloadRequest = None,
                          **kwargs) -> AsyncModelQueryable:
        return DocumentQueriedService(self.create_document(),
                                      addition=self.__get_addition(request.get_auth()),
                                      projection_model=self.create_project_document(),
                                      session=session)

    def _create_deletable(self, session: ClientSession | None = None,
                          request: ManagementIdPayloadRequest = None,
                          **kwargs) -> AsyncModelDeletable:
        return DocumentDeletableService(self.create_document(),
                                        additions=self.__get_addition(request.get_auth()),
                                        session=session)

    def _create_creatable(self, session: ClientSession | None = None,
                          request: ManagementPayloadRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        creatable = DocumentCreatableService(self.create_document(), session=session)
        creatable = DocumentLocaleCreatableService(creatable,
                                                   session=session,
                                                   locale=request.get_locale())

        auth_user = request.get_auth()
        return DocumentManagementCreatableService(creatable,
                                                  organization_ids=self._get_organization_ids(auth_user),
                                                  account_id=auth_user.id)

    def _create_updatable(self, session: ClientSession | None = None,
                          request: ManagementPayloadRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        auth_user = request.get_auth()
        updatable = DocumentUpdatableService(self.create_document(),
                                             additions=self.__get_addition(auth_user),
                                             session=session)
        updatable = DocumentLocaleUpdatableService(updatable,
                                                   session=session,
                                                   locale=request.get_locale())
        return DocumentManagementUpdatableService(updatable,
                                                  organization_ids=self._get_organization_ids(auth_user),
                                                  account_id=auth_user.id)

    def __get_addition(self, current_user: AuthenticationUser | None):
        addition = dict()
        if current_user:
            organization_ids = self._get_organization_ids(current_user)
            addition['organization_id'] = {'$in': organization_ids}

        return addition

    @staticmethod
    def _get_organization_ids(current_user: AuthenticationUser):
        return [organization.id for organization in current_user.organizations]


class AdditionDeleteIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: DeleteSchema | List[DeleteSchema],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class AdditionManagementResource(ManagementResource):
    """
    For resource without the need of locale and translation
    """

    async def get(self, request=Depends(AuthURLParamsRequest)):
        return await super().get(request)

    async def delete(self, request=Depends(AdditionDeleteIdPayloadRequest)):
        return await super().delete(request)

    def _create_creatable(self, session: ClientSession | None = None,
                          request: ManagementPayloadRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        creatable = DocumentCreatableService(self.create_document(), session=session)
        auth_user = request.get_auth()
        return DocumentManagementCreatableService(creatable,
                                                  organization_ids=self._get_organization_ids(auth_user),
                                                  account_id=auth_user.id)

    def _create_updatable(self, session: ClientSession | None = None,
                          request: ManagementPayloadRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        auth_user = request.get_auth()
        updatable = DocumentUpdatableService(self.create_document(),
                                             additions=self.__get_addition(auth_user),
                                             session=session)
        return DocumentManagementUpdatableService(updatable,
                                                  organization_ids=self._get_organization_ids(auth_user),
                                                  account_id=auth_user.id)
