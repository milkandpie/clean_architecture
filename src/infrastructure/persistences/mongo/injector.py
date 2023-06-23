from pymongo.client_session import ClientSession

from src.applications import (
    BillingProducer,
    InternalProducer,
    BasedRepositoryInjector,
)
from src.infrastructure.producers import (
    KafkaBillingProducer,
    KafkaInternalProducer
)


class MongoRepositoryInjector(BasedRepositoryInjector):
    def __init__(self):
        super().__init__({
            ClientSession: None,
            BillingProducer: KafkaBillingProducer,
            InternalProducer: KafkaInternalProducer,
            BasedRepositoryInjector: MongoRepositoryInjector,
        })
