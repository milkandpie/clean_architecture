import asyncio

from src.api.consumers.command_types import BILLING_EVENTS
from src.api.consumers.common import BasedConsumerRunner, ConfiguredKafkaConsumer
from src.api.consumers.config import AnotherEventConsumerKafkaConfig
from src.applications import MediatorGetter
from src.infrastructure import init_collections, MongoRepositoryInjector

if __name__ == '__main__':
    consumer = ConfiguredKafkaConsumer(AnotherEventConsumerKafkaConfig())
    runner = BasedConsumerRunner(consumer, BILLING_EVENTS, MediatorGetter, MongoRepositoryInjector(),
                                 worker_name='Another event')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_collections())
    loop.run_until_complete(runner.consume())
