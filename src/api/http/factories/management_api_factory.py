from beanie import init_beanie
from fastapi import FastAPI

from apps.http.resources.managements import resources as management_resources
from common import MongoClientFactory
from config import (
    API_DEBUG,
    MANAGEMENT_MONGO_CONFIG)
from models import management
from .api_factory import (
    APIFactory,
    APICreatable)


class ManagementAPIFactory(APICreatable):
    def __init__(self):
        self.__factory = APIFactory([*management_resources],
                                    name='Management resource',
                                    # prefix='management',
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        app = self.__factory.create_app()

        @app.on_event('startup')
        async def collections_initialized():
            client = MongoClientFactory().create(MANAGEMENT_MONGO_CONFIG)
            await init_beanie(
                getattr(client, MANAGEMENT_MONGO_CONFIG['db']),
                document_models=[management.ManagementDocument,
                                 management.ManagementNotable,
                                 management.ManagementEvent,
                                 management.ManagementApprovedOrder,
                                 management.ManagementOrderStatus,
                                 management.ManagementArtifact,
                                 management.ManagementFile,
                                 management.ManagementCategory,
                                 management.ManagementExtra,
                                 management.ManagementStorageOrigin,
                                 management.ManagementStorageState,
                                 management.ManagementTranslation])

        return app
