from fastapi import Depends

from apps.http.requests import ManagementFileRequest
from apps.http.resources.storage_resource import StorageResource
from config import (
    MINIO_URL,
    MINIO_SECURE,
    MANAGEMENT_BUCKET,
    MANAGEMENT_MINIO_CONFIG)
from services import (
    StorageUploaded,
    MinioStorageAdapter)


class ManagementStorageResource(StorageResource):
    async def put(self, request: ManagementFileRequest = Depends(ManagementFileRequest)):
        return await super().put(request)

    def _create_uploaded(self) -> StorageUploaded:
        return MinioStorageAdapter(MANAGEMENT_BUCKET, MINIO_URL, MANAGEMENT_MINIO_CONFIG,
                                   secure=MINIO_SECURE)
