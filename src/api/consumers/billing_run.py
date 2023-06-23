import asyncio

from src.api.consumers.command_types import BILLING_EVENTS
from src.api.consumers.common import BasedConsumerRunner, ConfiguredKafkaConsumer
from src.api.consumers.config import BillingEventConsumerKafkaConfig
from src.infrastructure import init_collections

if __name__ == '__main__':
    consumer = ConfiguredKafkaConsumer(BillingEventConsumerKafkaConfig())
    runner = BasedConsumerRunner(consumer, BILLING_EVENTS, worker_name='Billing event')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_collections())
    loop.run_until_complete(runner.consume())
