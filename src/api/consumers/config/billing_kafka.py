from dataclasses import dataclass
from logging import getLogger

from decouple import config

from src.infrastructure import KafkaSSLConfig
from .general import KafkaConsumerConfig

log = getLogger(__name__)
# Kafka
BILLING_EVENT_TOPIC = config('BILLING_EVENT_TOPIC', None)
BILLING_EVENT_GROUP_ID = config('BILLING_EVENT_GROUP_ID', None)


# SSL configuration
@dataclass()
class BillingConsumerKafkaSSLConfig(KafkaSSLConfig):
    security_protocol: str = config('BILLING_SECURITY_PROTOCOL', 'SASL_SSL')
    ssl_check_hostname: str = bool(int(config('BILLING_SSL_CHECK_HOSTNAME', False)))
    ssl_cafile: str = config('BILLING_SSL_CA_FILE', None)
    sasl_mechanism: str = config('BILLING_SASL_MECHANISM', 'PLAIN')
    sasl_plain_username: str = config('BILLING_SASL_PLAIN_USERNAME', 'username')
    sasl_plain_password: str = config('BILLING_SASL_PLAIN_PASSWORD', 'password')


@dataclass()
class BillingEventConsumerKafkaConfig(KafkaConsumerConfig):
    topic_id: str = config('BILLING_EVENT_TOPIC', 'event')
    group_id: str = config('BILLING_EVENT_GROUP_ID', 'event')
    bootstrap_servers: str = config('BILLING_KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    ssl_enabled: bool = bool(int(config('BILLING_ENABLE_KAFKA_SSL', False)))
    ssl_config: BillingConsumerKafkaSSLConfig = BillingConsumerKafkaSSLConfig()
