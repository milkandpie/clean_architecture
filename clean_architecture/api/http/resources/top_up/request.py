from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic import BaseModel

from clean_architecture.api.http.common import AuthPayloadRequest, UserAuthRequest


class TopUpModel(BaseModel):
    amount: int
    comment: str
    executed_at: datetime


class TopUpRequest(AuthPayloadRequest):
    def __init__(self, payload: TopUpModel | List[TopUpModel],
                 auth=Depends(UserAuthRequest)):
        super().__init__(payload, auth)
