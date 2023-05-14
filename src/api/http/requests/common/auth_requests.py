from abc import (
    ABC,
    abstractmethod)
from typing import (
    Tuple,
    List)

from fastapi import Request, Header, Depends, UploadFile
from pydantic import BaseModel

from services.integrations.auth import (
    AuthenticationUser,
    AccountTokenDecodedService,
    OrganizationDecodedService)
from .requests import (
    IdRequest,
    IdRequested,
    BasedRequest,
    PayloadRequest,
    RequestGettable,
    PayloadRequested,
    URLParamsRequest,
    URLParamsRequested)
from .stream_request import (
    FileRequested,
    FileRequest)


class AuthRequested(ABC):
    @abstractmethod
    def get_auth(self) -> AuthenticationUser:
        pass


class UserAuthRequest(AuthRequested):
    def __init__(self, authorization=Header(...)):
        decoded_service = AccountTokenDecodedService(authorization)
        self.__auth_user = decoded_service.generate()

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_user


class OrganizationAuthRequest(AuthRequested):
    def __init__(self, authorization=Header(...), x_organization_id=Header(...)):
        decoded_service = AccountTokenDecodedService(authorization)
        decoded_service = OrganizationDecodedService(decoded_service, x_organization_id)
        self.__auth_user = decoded_service.generate()

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_user


class BasedAuthRequest(RequestGettable, AuthRequested):
    def __init__(self, auth_request: AuthRequested = Depends(UserAuthRequest),
                 based_requested: RequestGettable = Depends(BasedRequest)):
        self.__based_request = based_requested
        self.__auth_requested = auth_request

    def get_request(self) -> Request:
        return self.__based_request.get_request()

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_requested.get_auth()


class AuthURLParamsRequest(IdRequested, RequestGettable, URLParamsRequested, AuthRequested):
    def __init__(self, auth_requested: AuthRequested = Depends(UserAuthRequest),
                 requested: URLParamsRequest = Depends(URLParamsRequest)):
        self.__requested = requested
        self.__auth_requested = auth_requested

    def get_request(self) -> Request:
        return self.__requested.get_request()

    def get_auth(self):
        return self.__auth_requested.get_auth()

    def get_query(self) -> str | None:
        return self.__requested.get_query()

    def get_id(self) -> str | None:
        return self.__requested.get_id()

    def get_sort(self) -> Tuple[str, int] | None:
        return self.__requested.get_sort()

    def get_limit(self) -> int:
        return self.__requested.get_limit()

    def get_offset(self) -> int:
        return self.__requested.get_offset()

    def get_filters(self) -> dict:
        return self.__requested.get_filters()


class AuthIdRequest(IdRequested, RequestGettable, AuthRequested):
    def __init__(self, auth_requested: AuthRequested = Depends(UserAuthRequest),
                 requested: IdRequest = Depends(IdRequest)):
        self.__requested = requested
        self.__auth_requested = auth_requested

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_requested.get_auth()

    def get_request(self) -> Request:
        return self.__requested.get_request()

    def get_id(self) -> str | None:
        return self.__requested.get_id()


class AuthPayloadRequest(PayloadRequested, AuthRequested):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 auth_requested: AuthRequested = Depends(UserAuthRequest)):
        self.__payload_requested = PayloadRequest(payload)
        self.__auth_requested = auth_requested

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return await self.__payload_requested.get_payload()

    def get_auth(self):
        return self.__auth_requested.get_auth()


class AuthIdPayloadRequest(IdRequested, PayloadRequested, AuthRequested, RequestGettable):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 params_requested: AuthIdRequest = Depends(AuthIdRequest)):
        self.__payload_requested = PayloadRequest(payload)
        self.__auth_requested = params_requested

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return await self.__payload_requested.get_payload()

    def get_request(self) -> Request:
        return self.__auth_requested.get_request()

    def get_id(self) -> str | None:
        return self.__auth_requested.get_id()

    def get_auth(self):
        return self.__auth_requested.get_auth()


class AuthFileRequest(AuthRequested, FileRequested):
    def __init__(self, auth_requested: AuthRequested = Depends(UserAuthRequest),
                 requested: FileRequested = Depends(FileRequest)):
        self.__auth_requested = auth_requested
        self.__requested = requested

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_requested.get_auth()

    def get_files(self) -> List[UploadFile]:
        return self.__requested.get_files()
