from dataclasses import dataclass
from logging import getLogger

from decouple import config

from clean_architecture.infrastructure import KafkaSSLConfig
from .general import KafkaConsumerConfig

log = getLogger(__name__)
# Kafka
ANOTHER_EVENT_TOPIC = config('ANOTHER_EVENT_TOPIC', None)
ANOTHER_EVENT_GROUP_ID = config('ANOTHER_EVENT_GROUP_ID', None)


# SSL configuration
@dataclass()
class AnotherConsumerKafkaSSLConfig(KafkaSSLConfig):
    security_protocol: str = config('ANOTHER_SECURITY_PROTOCOL', 'SASL_SSL')
    ssl_check_hostname: str = bool(int(config('ANOTHER_SSL_CHECK_HOSTNAME', False)))
    ssl_cafile: str = config('ANOTHER_SSL_CA_FILE', None)
    sasl_mechanism: str = config('ANOTHER_SASL_MECHANISM', 'PLAIN')
    sasl_plain_username: str = config('ANOTHER_SASL_PLAIN_USERNAME', 'username')
    sasl_plain_password: str = config('ANOTHER_SASL_PLAIN_PASSWORD', 'password')


@dataclass()
class AnotherEventConsumerKafkaConfig(KafkaConsumerConfig):
    topic_id: str = config('ANOTHER_EVENT_TOPIC', 'event')
    group_id: str = config('ANOTHER_EVENT_GROUP_ID', 'event')
    bootstrap_servers: str = config('ANOTHER_KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    ssl_enabled: bool = bool(int(config('ANOTHER_ENABLE_KAFKA_SSL', False)))
    ssl_config: AnotherConsumerKafkaSSLConfig = AnotherConsumerKafkaSSLConfig()
