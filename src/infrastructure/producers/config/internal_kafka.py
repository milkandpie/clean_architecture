from dataclasses import dataclass
from logging import getLogger

from decouple import config

from .billing_kafka import KafkaSSLConfig, KafkaProducerConfig

log = getLogger(__name__)

INTERNAL_EVENT_TOPIC = config('INTERNAL_EVENT_TOPIC', None)


@dataclass()
class InternalKafkaSSLConfig(KafkaSSLConfig):
    security_protocol: str = config('INTERNAL_SECURITY_PROTOCOL', 'SASL_SSL')
    ssl_check_hostname: str = bool(int(config('INTERNAL_SSL_CHECK_HOSTNAME', False)))
    ssl_cafile: str = config('INTERNAL_SSL_CA_FILE', None)
    sasl_mechanism: str = config('INTERNAL_SASL_MECHANISM', 'PLAIN')
    sasl_plain_username: str = config('INTERNAL_SASL_PLAIN_USERNAME', 'username')
    sasl_plain_password: str = config('INTERNAL_SASL_PLAIN_PASSWORD', 'password')


@dataclass
class InternalKafkaProducerConfig(KafkaProducerConfig):
    bootstrap_servers: str = config('INTERNAL_KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    ssl_enabled: bool = bool(int(config('INTERNAL_ENABLE_KAFKA_SSL', False)))
    ssl_config: InternalKafkaSSLConfig = InternalKafkaSSLConfig()
