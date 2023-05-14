from abc import ABC
from typing import List

from fastapi import Depends

from apps.http.requests import (
    DeleteSchema,
    AdminIdRequest,
    AdminParamsRequest,
    AdminPayloadRequest,
    AdminIdPayloadRequest)
from apps.http.resources.base_resource import BaseResource


class DeleteIdPayloadRequest(AdminIdPayloadRequest):
    def __init__(self, payload: DeleteSchema | List[DeleteSchema],
                 requested=Depends(AdminIdRequest)):
        super().__init__(payload, requested)


class AuthResource(BaseResource, ABC):

    async def get(self, request=Depends(AdminParamsRequest)):
        return await super(AuthResource, self).get(request)

    async def post(self, request=Depends(AdminPayloadRequest)):
        return await super(AuthResource, self).post(request)

    async def patch(self, request=Depends(AdminIdPayloadRequest)):
        return await super(AuthResource, self).patch(request)

    async def delete(self, request=Depends(DeleteIdPayloadRequest)):
        return await super(AuthResource, self).delete(request)
