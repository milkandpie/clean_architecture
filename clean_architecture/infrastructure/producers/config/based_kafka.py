from dataclasses import dataclass
from logging import getLogger

from decouple import config

log = getLogger(__name__)


@dataclass()
class KafkaSSLConfig:
    security_protocol: str
    ssl_check_hostname: str
    ssl_cafile: str
    sasl_mechanism: str
    sasl_plain_username: str
    sasl_plain_password: str


@dataclass
class KafkaProducerConfig:
    bootstrap_servers: str
    ssl_enabled: bool
    ssl_config: KafkaSSLConfig


EVENT_TOPIC = config('EXTERNAL_EVENT_TOPIC', None)


@dataclass()
class AnotherKafkaSSLConfig(KafkaSSLConfig):
    security_protocol: str = config('SECURITY_PROTOCOL', 'SASL_SSL')
    ssl_check_hostname: str = bool(int(config('SSL_CHECK_HOSTNAME', False)))
    ssl_cafile: str = config('SSL_CA_FILE', None)
    sasl_mechanism: str = config('SASL_MECHANISM', 'PLAIN')
    sasl_plain_username: str = config('SASL_PLAIN_USERNAME', 'username')
    sasl_plain_password: str = config('SASL_PLAIN_PASSWORD', 'password')


@dataclass
class AnotherKafkaProducerConfig(KafkaProducerConfig):
    bootstrap_servers: str = config('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    ssl_enabled: bool = bool(int(config('ENABLE_KAFKA_SSL', False)))
    ssl_config: AnotherKafkaSSLConfig = AnotherKafkaSSLConfig()
