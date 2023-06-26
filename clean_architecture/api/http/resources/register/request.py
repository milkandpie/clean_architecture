from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic import BaseModel

from clean_architecture.api.http.common import BasedPayloadRequest, BasedRequest


class RegisterModel(BaseModel):
    name: str
    email: str
    password: str
    executed_at: datetime


class RegisterRequest(BasedPayloadRequest):
    def __init__(self, payload: RegisterModel | List[RegisterModel],
                 params_requested=Depends(BasedRequest)):
        super().__init__(payload, params_requested)
