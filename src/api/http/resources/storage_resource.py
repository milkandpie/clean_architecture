from abc import abstractmethod

from fastapi import Depends

from apps.http.requests import (
    FileRequest,
    FileRequested)
from services import StorageUploaded
from .resource import Resource


class StorageResource(Resource):
    def __init__(self, path: str = None):
        super(StorageResource, self).__init__()
        path = path or '/upload'
        self.router.add_api_route(path, self.put, methods=['PUT'], status_code=200)

    async def put(self, request: FileRequested = Depends(FileRequest)):
        results = []
        uploaded = self._create_uploaded()
        for file in request.get_files():
            results.append(await uploaded.upload(file))

        return {'_item': results, '_meta': {'total': len(results)}}

    @abstractmethod
    def _create_uploaded(self) -> StorageUploaded:
        pass
