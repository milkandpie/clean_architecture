import asyncio

from clean_architecture.api.consumers.command_types import BILLING_EVENTS
from clean_architecture.api.consumers.common import BasedConsumerRunner, ConfiguredKafkaConsumer
from clean_architecture.api.consumers.config import AnotherEventConsumerKafkaConfig
from clean_architecture.infrastructure import init_collections

if __name__ == '__main__':
    consumer = ConfiguredKafkaConsumer(AnotherEventConsumerKafkaConfig())
    runner = BasedConsumerRunner(consumer, BILLING_EVENTS, worker_name='Another event')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_collections())
    loop.run_until_complete(runner.consume())
