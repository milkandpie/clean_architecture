from pymongo.client_session import ClientSession

from src.applications import (
    AnotherProducer,
    InternalProducer,
    BasedRepositoryInjector,
)
from src.infrastructure.producers import (
    KafkaAnotherProducer,
    KafkaInternalProducer
)


class MongoRepositoryInjector(BasedRepositoryInjector):
    def __init__(self):
        super().__init__({
            ClientSession: None,
            AnotherProducer: KafkaAnotherProducer,
            InternalProducer: KafkaInternalProducer,
            BasedRepositoryInjector: MongoRepositoryInjector,
        })
