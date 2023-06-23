from src.applications import BillingProducer, BillingMessage
from ._producer import ConfiguredKafkaProducer, KafkaMessage, ProducerRunner
from .config import BillingKafkaProducerConfig, BILLING_EVENT_TOPIC


class KafkaBillingProducer(BillingProducer):
    def __init__(self):
        self.__producer = ProducerRunner(ConfiguredKafkaProducer(BILLING_EVENT_TOPIC, BillingKafkaProducerConfig()))

    def send_message(self, message: BillingMessage):
        self.__producer.send_message(KafkaMessage(
            key=message.key,
            payload=message.payload,
            issued_at=message.issued_at,
            event_type=message.event_type,
            raw_message=message.raw_message))
