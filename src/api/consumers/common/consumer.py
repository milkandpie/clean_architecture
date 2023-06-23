import json
from abc import ABC, abstractmethod
from asyncio import sleep
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger, INFO, StreamHandler
from typing import List, Any, Tuple

from pydantic import ValidationError
from kafka import KafkaConsumer
from kafka.structs import (
    TopicPartition,
    OffsetAndMetadata)

from src.api.consumers.config import (
    CONSUMER_RETRY,
    KafkaConsumerConfig)
from src.domains import (
    Event,
    DomainException,
    IncorrectDomainValuedException)
from src.applications import MediatorGetter
from src.infrastructure import MongoRepositoryInjector
from .dataclass_to_based_model import convert_flat_dataclass_to_pydantic

log = getLogger(__name__)
log.setLevel(INFO)
log.addHandler(StreamHandler())


class InvalidMessageException(Exception):
    pass


@dataclass
class ConsumedMessage:
    payload: dict
    event_type: str
    based_message: Any
    issued_at: datetime | None


class Consumer(ABC):
    @abstractmethod
    def poll(self) -> List[ConsumedMessage]:
        pass

    @abstractmethod
    def send_ack(self, message):
        pass


class BasedConsumerRunner:
    def __init__(self, consumer: Consumer, command_types: dict,
                 worker_name: str = None):
        log.info('Running %s consumer', worker_name or 'a long cycle system')
        self.__consumer = consumer
        self.__command_types = self.__make_handlers(command_types)

    @staticmethod
    def __make_handlers(command_types: dict) -> dict:
        new_command_types = {}
        for event_name, command_type in command_types.items():
            if (isinstance(command_type, dict) and
                    command_type.get('command_type') and command_type.get('based_model_type')):
                new_command_types[event_name] = command_type
                continue

            if isinstance(command_type, type(Event)):
                new_command_types[event_name] = {
                    'command_type': command_type,
                    # Convert command to Pydantic model to validate and sanitize data
                    'based_model_type': convert_flat_dataclass_to_pydantic(command_type)
                }

        return new_command_types

    async def consume(self):
        while True:
            messages = self.__consumer.poll()
            if not messages:
                await sleep(0.5)
                continue

            for message in messages:
                event_data = self.__command_types.get(message.event_type)
                if not event_data:
                    self.__consumer.send_ack(message.based_message)
                    continue

                event_retry = CONSUMER_RETRY
                while True:
                    try:
                        based_model = event_data['based_model_type'](**message.payload)
                        command = event_data['command_type'](**based_model.dict())
                        mediator = MediatorGetter.get_mediator('command', injector=MongoRepositoryInjector())
                        await mediator.handle(command)
                        break

                    except (TypeError, ValidationError) as e:
                        log.warning('Invalid command payload. Error: %s', e)
                        self.__consumer.send_ack(message.based_message)
                        break

                    except InvalidMessageException as e:
                        log.warning('Invalid event. Error: %s', e)
                        self.__consumer.send_ack(message.based_message)
                        break

                    except (IncorrectDomainValuedException, DomainException) as e:
                        log.error(e)
                        self.__consumer.send_ack(message.based_message)
                        break

                    except Exception as e:
                        event_retry -= 1
                        await sleep(0.5)
                        log.warning('Retry: %s/%s. Unexpected error: %s', event_retry, CONSUMER_RETRY, str(e))
                        if event_retry <= 0:
                            raise e

                self.__consumer.send_ack(message.based_message)


@dataclass
class KafkaConsumedMessage(ConsumedMessage):
    based_message = Tuple[TopicPartition, Any]


class ConfiguredKafkaConsumer(Consumer):
    def __init__(self, config: KafkaConsumerConfig,
                 auto_commit: bool = True):
        log.warning('Listen to %s on %s', config.group_id, config.bootstrap_servers)

        self.__consumer = KafkaConsumer(config.topic_id, **{
            'group_id': config.group_id,
            'enable_auto_commit': auto_commit,
            'bootstrap_servers': config.bootstrap_servers,
            **(config.ssl_config if config.ssl_enabled else {})
        })

    def send_ack(self, based_message):
        topic_partition, message = based_message
        self.__consumer.commit({topic_partition: OffsetAndMetadata(message.offset + 1, "no metadata")})

    def poll(self) -> List[KafkaConsumedMessage]:
        message_batch = self.__consumer.poll(300, 1)

        messages = []
        for topic_partition, partition_batch in message_batch.items():
            for message in partition_batch:
                body = message.value
                body = json.loads(body.decode('utf-8'))
                try:
                    payload = body['payload']
                    event_type = body['event_type']
                    issued_at = body.get('issued_at')

                except KeyError as e:
                    raise InvalidMessageException() from e
                messages.append(KafkaConsumedMessage(payload, event_type, (topic_partition, message), issued_at))

        return messages
