from typing import Type, List

from beanie import Document
from fastapi import Depends
from pymongo.client_session import ClientSession

from apps.http.requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthIdRequest,
    UserAuthRequest)
from models.management import ManagementApprovedOrder
from services import (
    ApprovedOrderUpdatableService,
    ApprovedOrderCreatedService,
    ApprovedOrderQueriedService,
    AsyncModelCreatable,
    AsyncModelUpdatable,
    AsyncModelQueryable)
from ._management_resource import (
    AdditionManagementResource,
    ManagementExtraIn)


class ApprovedOrderIn(ManagementExtraIn):
    status_id: str


class ApprovedOrderPayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: ApprovedOrderIn | List[ApprovedOrderIn],
                 requested=Depends(UserAuthRequest)):
        super().__init__(payload, requested)


class ApprovedOrderIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: ApprovedOrderIn | List[ApprovedOrderIn],
                 requested=Depends(AuthIdRequest)):
        super().__init__(payload, requested)


class ApprovedOrderResource(AdditionManagementResource):
    def __init__(self):
        super(ApprovedOrderResource, self).__init__('/approved_orders')

    def create_document(self) -> Type[Document]:
        return ManagementApprovedOrder

    def _create_creatable(self, session: ClientSession = None,
                          request: ApprovedOrderPayloadRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        creatable = super(ApprovedOrderResource, self)._create_creatable(session=session, request=request, **kwargs)
        return ApprovedOrderCreatedService(creatable, request.get_auth().id,
                                           session=session)

    def _create_updatable(self, session: ClientSession | None = None,
                          request: ApprovedOrderPayloadRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        updatable = super()._create_updatable(session=session, request=request, **kwargs)
        return ApprovedOrderUpdatableService(updatable, request.get_auth().id,
                                             session=session)

    def _create_queryable(self, session: ClientSession | None = None,
                          request: AuthPayloadRequest = None,
                          **kwargs) -> AsyncModelQueryable:
        queried = super()._create_queryable(session, request, **kwargs)
        return ApprovedOrderQueriedService(queried,
                                           session=session)

    async def post(self, request=Depends(ApprovedOrderPayloadRequest)):
        return await super(ApprovedOrderResource, self).post(request)

    async def patch(self, request=Depends(ApprovedOrderIdPayloadRequest)):
        return await super(ApprovedOrderResource, self).patch(request)
