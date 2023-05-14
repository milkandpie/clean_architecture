from abc import ABC, abstractmethod
from typing import List

from fastapi import (
    Query,
    Depends)
from pydantic import BaseModel

from constants import VI_LOCALE
from services import AuthenticationUser
from .common import (
    AuthIdPayloadRequest,
    AuthURLParamsRequest,
    AuthPayloadRequest,
    URLParamsRequest,
    UserAuthRequest,
    AuthFileRequest,
    AuthIdRequest,
    AuthRequested,
    FileRequest,
    IdRequest)


class ManagementRequested(ABC):
    @abstractmethod
    def get_locale(self) -> str:
        pass


class ManagementRequest(ManagementRequested, AuthRequested):
    def __init__(self, auth_requested: UserAuthRequest = Depends(UserAuthRequest),
                 locale: str = Query(description='Locale parameter translation query and command',
                                     default=VI_LOCALE)):
        self.__auth_requested = auth_requested
        self.__locale = locale

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_requested.get_auth()

    def get_locale(self) -> str:
        return self.__locale


class ManagementParamsRequest(AuthURLParamsRequest, ManagementRequested):
    def __init__(self,
                 requested: URLParamsRequest = Depends(URLParamsRequest),
                 management_requested: ManagementRequest = Depends(ManagementRequest)):
        super().__init__(management_requested, requested)
        self.__management_requested = management_requested

    def get_locale(self) -> str:
        return self.__management_requested.get_locale()


class ManagementIdRequest(AuthIdRequest, ManagementRequested):
    def __init__(self, requested: IdRequest = Depends(IdRequest),
                 management_requested: ManagementRequest = Depends(ManagementRequest)):
        super().__init__(management_requested, requested)
        self.__management_requested = management_requested

    def get_locale(self) -> str:
        return self.__management_requested.get_locale()


class ManagementPayloadRequest(AuthPayloadRequest, ManagementRequested):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 management_requested: ManagementRequest = Depends(ManagementRequest)):
        super().__init__(payload, auth_requested=management_requested)
        self.__management_requested = management_requested

    def get_locale(self) -> str:
        return self.__management_requested.get_locale()


class ManagementIdPayloadRequest(AuthIdPayloadRequest, ManagementRequested):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 params_requested: ManagementIdRequest = Depends(ManagementIdRequest)):
        super().__init__(payload, params_requested=params_requested)
        self.__management_requested = params_requested

    def get_locale(self) -> str:
        return self.__management_requested.get_locale()


class ManagementFileRequest(AuthFileRequest, ManagementRequested):
    def __init__(self, auth_requested: ManagementRequest = Depends(ManagementRequest),
                 requested: FileRequest = Depends(FileRequest)):
        super().__init__(auth_requested, requested)
        self.__management_requested = auth_requested

    def get_locale(self) -> str:
        return self.__management_requested.get_locale()
