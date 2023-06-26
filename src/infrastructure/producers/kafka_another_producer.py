from src.applications import AnotherProducer, AnotherMessage
from ._producer import ConfiguredKafkaProducer, KafkaMessage, ProducerRunner
from .config import AnotherKafkaProducerConfig, EVENT_TOPIC


class KafkaAnotherProducer(AnotherProducer):
    def __init__(self):
        self.__producer = ProducerRunner(ConfiguredKafkaProducer(EVENT_TOPIC, AnotherKafkaProducerConfig()))

    def send_message(self, message: AnotherMessage):
        self.__producer.send_message(KafkaMessage(
            key=message.key,
            payload=message.payload,
            issued_at=message.issued_at,
            event_type=message.event_type,
            raw_message=message.raw_message))
