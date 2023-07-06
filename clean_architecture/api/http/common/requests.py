from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from fastapi import Depends, Header
from pydantic import BaseModel


@dataclass
class AuthenticationUser:
    tenant_id: str


class AuthRequested(ABC):
    @abstractmethod
    def get_auth(self) -> AuthenticationUser:
        pass


class UserAuthRequest(AuthRequested):
    def __init__(self, authorization=Header(...)):
        self.__auth_user = AuthenticationUser(tenant_id='1')

    def get_auth(self) -> AuthenticationUser:
        return self.__auth_user


class PayloadRequested(ABC):
    @abstractmethod
    async def get_payload(self) -> BaseModel | List[BaseModel]:
        pass


class PayloadRequest(PayloadRequested):
    def __init__(self, payload: BaseModel | List[BaseModel]):
        self.__payload = payload

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return self.__payload


class AuthPayloadRequest(PayloadRequested, AuthRequested):
    def __init__(self, payload: BaseModel | List[BaseModel],
                 auth_requested: AuthRequested = Depends(UserAuthRequest)):
        self.__payload_requested = PayloadRequest(payload)
        self.__auth_requested = auth_requested

    async def get_payload(self) -> BaseModel | List[BaseModel]:
        return await self.__payload_requested.get_payload()

    def get_auth(self):
        return self.__auth_requested.get_auth()
