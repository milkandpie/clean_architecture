from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    ManagementIdPayloadRequest,
    ManagementPayloadRequest,
    ManagementIdRequest,
    ManagementRequest)
from models.management import ManagementEvent
from ._management_resource import (
    ManagementResource,
    ManagementIn)


class EventIn(ManagementIn):
    type: str = 'event'


class EventPayloadRequest(ManagementPayloadRequest):
    def __init__(self, payload: EventIn | List[EventIn],
                 requested: ManagementRequest = Depends(ManagementRequest)):
        super().__init__(payload, requested)


class EventIdPayloadRequest(ManagementIdPayloadRequest):
    def __init__(self, payload: EventIn | List[EventIn],
                 requested: ManagementIdRequest = Depends(ManagementIdRequest)):
        super().__init__(payload, requested)


class EventResource(ManagementResource):
    def __init__(self):
        super(EventResource, self).__init__('/events')

    def create_document(self) -> Type[Document]:
        return ManagementEvent

    async def post(self, request=Depends(EventPayloadRequest)):
        return await super(EventResource, self).post(request=request)

    async def patch(self, request=Depends(EventIdPayloadRequest)):
        return await super(EventResource, self).patch(request=request)
