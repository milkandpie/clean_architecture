from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Type

from src.domains import DomainEvent, IntegrationEvent
from .common import EventHandleable


@dataclass
class Message:
    payload: dict
    event_type: str
    raw_message: DomainEvent = None
    issued_at: datetime = None

    @staticmethod
    def from_integration(event: IntegrationEvent) -> 'Message':
        return Message(payload={**event.payload,
                                'event_id': event.event_id},
                       event_type=event.event_name)


class Producer(ABC):
    """
    Producer API for sending and publishing message
    """

    @abstractmethod
    def send_message(self, message: Message):
        pass


@dataclass
class AnotherMessage(Message):
    key: str = None

    @staticmethod
    def from_integration(event: IntegrationEvent) -> 'AnotherMessage':
        return AnotherMessage(payload=event.payload,
                              event_type=event.event_name,
                              key=event.key)


class AnotherProducer(Producer, ABC):
    @abstractmethod
    def send_message(self, message: AnotherMessage):
        pass


class EventIntegratedHandler(EventHandleable):
    def __init__(self, producer: Producer, message_type: Type[Message]):
        self.__producer: Producer = producer
        self.__message_type = message_type

    async def handle(self, event: DomainEvent):
        integration_event = event.to_integration(event.create_event_name())
        integration_event.key = str(event.aggregate_id)

        self.__producer.send_message(self.__message_type.from_integration(integration_event))


class EventBillingIntegratedHandler(EventIntegratedHandler):
    def __init__(self, producer: AnotherProducer):
        super().__init__(producer, AnotherMessage)


@dataclass()
class InternalMessage(Message):
    key: str = None

    @staticmethod
    def from_integration(event: IntegrationEvent) -> 'InternalMessage':
        return InternalMessage(payload={**event.payload,
                                        'event_id': event.event_id,
                                        'aggregate_id': event.aggregate_id,
                                        'aggregate_name': event.aggregate_name},
                               event_type=event.event_name,
                               key=event.key)


class InternalProducer(Producer, ABC):
    @abstractmethod
    def send_message(self, message: AnotherMessage):
        pass


class InternalEventHandler(EventIntegratedHandler):
    def __init__(self, producer: InternalProducer):
        super().__init__(producer, InternalMessage)
