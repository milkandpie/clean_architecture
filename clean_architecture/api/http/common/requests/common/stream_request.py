from abc import ABC, abstractmethod
from typing import List

from fastapi import (Depends, UploadFile)
from starlette.requests import Request

from .requests import (
    BasedRequest,
    RequestGettable)


class FileRequested(ABC):
    @abstractmethod
    def get_files(self) -> List[UploadFile]:
        pass


class FileRequest(FileRequested, RequestGettable):
    def __init__(self, files: List[UploadFile],
                 requested: RequestGettable = Depends(BasedRequest)):
        self.__files = files
        self.__requested = requested

    def get_request(self) -> Request:
        return self.__requested.get_request()

    def get_files(self) -> List[UploadFile]:
        return self.__files
