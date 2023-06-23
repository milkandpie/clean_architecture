from beanie import init_beanie

from .common import MongoClientFactory
from .config import GENERAL_MONGO_CONFIG
from .models import *


async def init_collections(config: dict = None):
    config = config or GENERAL_MONGO_CONFIG
    client = MongoClientFactory().create(config)
    await init_beanie(
        getattr(client, config['db']),
        document_models=[DelayedEventDocument, IntegrationEventDocument])
