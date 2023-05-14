from typing import Type, List

from beanie import Document
from fastapi import Depends
from pymongo.client_session import ClientSession

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementProject
from services import (
    ProjectCreatableService,
    ProjectUpdatableService,
    AsyncModelCreatable,
    AsyncModelUpdatable)
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class ProjectIn(ManagementIn):
    category_id: str
    type: str = 'project'


class ProjectPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: ProjectIn | List[ProjectIn],
                 requested=Depends(ManagementRequest)):
        super().__init__(payload, requested)


class ProjectIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: ProjectIn | List[ProjectIn],
                 requested=Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class ProjectResource(ManagementResource):
    def __init__(self):
        super(ProjectResource, self).__init__('/projects')

    def create_document(self) -> Type[Document]:
        return ManagementProject

    def _create_creatable(self, session: ClientSession = None,
                          **kwargs) -> AsyncModelCreatable:
        creatable = super(ProjectResource, self)._create_creatable(session=session, **kwargs)
        return ProjectCreatableService(creatable, session=session)

    def _create_updatable(self, session: ClientSession | None = None,
                          **kwargs) -> AsyncModelUpdatable:
        updatable = super(ProjectResource, self)._create_updatable(session=session, **kwargs)
        return ProjectUpdatableService(updatable, session=session)

    async def post(self, request=Depends(ProjectPayloadRequest)):
        return await super(ProjectResource, self).post(request)

    async def patch(self, request=Depends(ProjectIdPayloadRequest)):
        return await super(ProjectResource, self).patch(request)
