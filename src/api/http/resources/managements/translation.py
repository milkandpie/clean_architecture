from typing import Type, List

from beanie import Document
from fastapi import Depends

from apps.http.requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthIdRequest,
    UserAuthRequest)
from models.management import ManagementTranslation
from ._management_resource import (
    AdditionManagementResource,
    ManagementExtraIn)


class TranslationIn(ManagementExtraIn):
    name: str
    locale: str
    summary: str
    description: str
    data: dict = None


class TranslationPayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: TranslationIn | List[TranslationIn],
                 requested=Depends(UserAuthRequest)):
        super().__init__(payload, requested)


class TranslationIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: TranslationIn | List[TranslationIn],
                 requested=Depends(AuthIdRequest)):
        super().__init__(payload, requested)


class TranslationResource(AdditionManagementResource):
    def __init__(self):
        super(TranslationResource, self).__init__('/translations')

    def create_document(self) -> Type[Document]:
        return ManagementTranslation

    async def post(self, request=Depends(TranslationPayloadRequest)):
        return await super(TranslationResource, self).post(request)

    async def patch(self, request=Depends(TranslationIdPayloadRequest)):
        return await super(TranslationResource, self).patch(request)
