from dataclasses import dataclass

from clean_architecture.infrastructure import KafkaSSLConfig

CONSUMER_RETRY = 3


@dataclass
class KafkaConsumerConfig:
    group_id: str
    topic_id: str
    bootstrap_servers: str
    ssl_enabled: bool
    ssl_config: KafkaSSLConfig
