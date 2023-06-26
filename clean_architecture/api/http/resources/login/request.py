from typing import List

from fastapi import Depends
from pydantic import BaseModel

from clean_architecture.api.http.common import BasedPayloadRequest, BasedRequest


class LoginModel(BaseModel):
    email: str
    password: str


class LoginRequest(BasedPayloadRequest):
    def __init__(self, payload: LoginModel | List[LoginModel],
                 params_requested=Depends(BasedRequest)):
        super().__init__(payload, params_requested)
