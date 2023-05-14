from fastapi import Depends

from apps.http.requests import AdminFileRequest
from apps.http.resources.storage_resource import StorageResource
from config import (
    MINIO_URL,
    AUTH_BUCKET,
    MINIO_SECURE,
    AUTH_MINIO_CONFIG)
from services import StorageUploaded, MinioStorageAdapter


class AdminStorageResource(StorageResource):
    async def put(self, request: AdminFileRequest = Depends(AdminFileRequest)):
        return await super().put(request)

    def _create_uploaded(self) -> StorageUploaded:
        return MinioStorageAdapter(AUTH_BUCKET, MINIO_URL, AUTH_MINIO_CONFIG,
                                   secure=MINIO_SECURE)
