from typing import Type, List

from beanie import Document
from fastapi import Depends
from pymongo.client_session import ClientSession

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementProjectItem
from services import (
    ProjectItemCreatableService,
    ProjectItemUpdatableService,
    AsyncModelCreatable,
    AsyncModelUpdatable)
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class ProjectItemIn(ManagementIn):
    item_id: str
    item_type: str
    project_id: str


class ProjectItemPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: ProjectItemIn | List[ProjectItemIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class ProjectItemIDPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: ProjectItemIn | List[ProjectItemIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class ProjectItemResource(ManagementResource):
    def __init__(self):
        super(ProjectItemResource, self).__init__('/projects/items')

    def create_document(self) -> Type[Document]:
        return ManagementProjectItem

    def _create_creatable(self, session: ClientSession = None, **kwargs) -> AsyncModelCreatable:
        creatable = super(ProjectItemResource, self)._create_creatable(session=session, **kwargs)
        return ProjectItemCreatableService(creatable, session=session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        updatable = super(ProjectItemResource, self)._create_updatable(session=session, **kwargs)
        return ProjectItemUpdatableService(updatable, session=session)

    async def post(self, request=Depends(ProjectItemPayloadRequest)):
        return await super(ProjectItemResource, self).post(request)

    async def patch(self, request=Depends(ProjectItemIDPayloadRequest)):
        return await super(ProjectItemResource, self).patch(request)
