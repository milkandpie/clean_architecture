from typing import List

from fastapi import Depends, Header
from pydantic import BaseModel

from clean_architecture.infrastructure import (
    JWTTokenEncoder,
    AuthenticationUser)
from .auth_requests import (
    AuthIdPayloadRequest,
    AuthPayloadRequest,
    AuthURLParamsRequest,
    URLParamsRequest,
    AuthFileRequest,
    AuthRequested,
    AuthIdRequest,
    FileRequest,
    IdRequest)


class AdminAuthRequest(AuthRequested):
    def __init__(self, authorization=Header(...)):
        decoded_service = JWTTokenEncoder()
        # decoded_service = AdminTokenDecodedService(decoded_service)
        self.__auth_user = decoded_service.decode(authorization)

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_user


class AdminParamsRequest(AuthURLParamsRequest):
    def __init__(self, requested: URLParamsRequest = Depends(URLParamsRequest),
                 auth_requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(auth_requested, requested)


class AdminIdRequest(AuthIdRequest):
    def __init__(self, requested: IdRequest = Depends(IdRequest),
                 auth_requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(auth_requested, requested)


class AdminPayloadRequest(AuthPayloadRequest):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 auth_requested: AdminAuthRequest = Depends(AdminAuthRequest)):
        super().__init__(payload, auth_requested)


class AdminIdPayloadRequest(AuthIdPayloadRequest):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 params_requested: AdminIdRequest = Depends(AdminIdRequest)):
        super().__init__(payload, params_requested=params_requested)


class AdminFileRequest(AuthFileRequest):
    def __init__(self, auth_requested: AdminAuthRequest = Depends(AdminAuthRequest),
                 requested: FileRequest = Depends(FileRequest)):
        super().__init__(auth_requested, requested)
