import json
import logging
import time
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger, INFO

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from clean_architecture.applications import ISO_8601, Producer, Message
from clean_architecture.domains import ValueObject, Entity
from .config import KafkaProducerConfig

log = getLogger(__name__)
log.setLevel(INFO)
log.addHandler(logging.StreamHandler())


class ProducerRetriedException(Exception):
    pass


class ProducerRunner(Producer):
    def __init__(self, producer: Producer,
                 max_retry: int = 3,
                 delay: int = 1):
        self.__producer = producer
        self.__max_retry = max_retry
        self.__delay = delay

    def send_message(self, message: Message):
        retry_count = 0
        while True:
            log.info("Start sending message - %s", message)
            try:
                self.__producer.send_message(message)
                return True
            except ProducerRetriedException as e:
                log.warning("Send message failed - %s - %s", message, e, exc_info=True)
                if retry_count >= self.__max_retry:
                    return False

                retry_count += 1
                log.error("Retry %s/%s in %s seconds on message - %s", retry_count, self.__max_retry, self.__delay)
                time.sleep(self.__delay)

            except Exception as e:
                log.exception('Send message failed - %s - %s', message, e)
                return False


@dataclass()
class KafkaMessage(Message):
    key: str = None


class ConfiguredKafkaProducer(Producer):
    def __init__(self, topic: str, config: KafkaProducerConfig,
                 producer: KafkaProducer = None):
        self.__producer = producer or KafkaProducer(**{
            'bootstrap_servers': config.bootstrap_servers,
            **(asdict(config.ssl_config) if config.ssl_enabled else {})
        })
        self.__topic = topic

    def send_message(self, message: KafkaMessage):
        retry_count = 0
        payload = message.raw_message or dict(
            issued_at=message.issued_at or datetime.utcnow(),
            event_type=message.event_type,
            payload=message.payload)

        log.info("Start sending message - %s", payload)
        try:
            params = dict(value=json.dumps(payload, default=self.__json_serial).encode('utf-8'),
                          topic=self.__topic)
            if message.key:
                params['key'] = str(message.key).encode('utf-8')

            self.__producer.send(**params).get(30)
            return True
        except (KafkaTimeoutError, ConnectionResetError) as e:
            raise ProducerRetriedException() from e

    @staticmethod
    def __json_serial(obj):
        if isinstance(obj, datetime):
            return obj.strftime(ISO_8601)

        if isinstance(obj, (Entity, ValueObject)):
            return str(obj)

        raise TypeError("Type %s not serializable" % type(obj))
