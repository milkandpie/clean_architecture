from clean_architecture.applications import InternalMessage, InternalProducer
from ._producer import ConfiguredKafkaProducer, KafkaMessage, ProducerRunner
from .config import InternalKafkaProducerConfig, INTERNAL_EVENT_TOPIC


class KafkaInternalProducer(InternalProducer):
    def __init__(self):
        self.__producer = ProducerRunner(ConfiguredKafkaProducer(INTERNAL_EVENT_TOPIC, InternalKafkaProducerConfig()))

    def send_message(self, message: InternalMessage):
        self.__producer.send_message(KafkaMessage(
            key=message.key,
            payload=message.payload,
            issued_at=message.issued_at,
            event_type=message.event_type,
            raw_message=message.raw_message))
