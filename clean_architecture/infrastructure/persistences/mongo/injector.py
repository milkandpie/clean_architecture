from pymongo.client_session import ClientSession

from clean_architecture.applications import (
    AnotherProducer,
    InternalProducer,
    BasedRepositoryInjector,
)
from clean_architecture.infrastructure.producers import (
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
