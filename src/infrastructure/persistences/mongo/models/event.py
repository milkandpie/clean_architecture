from datetime import datetime
from typing import List

from beanie import Indexed
from pydantic import BaseModel

from ._based_document import BasedDocument


class IntegrationEventDocument(BasedDocument):
    id: Indexed(str)
    event_name: Indexed(str)
    aggregate_id: Indexed(str)
    issued_at: Indexed(datetime)

    key: str
    payload: dict
    aggregate_name: str

    class Settings(BasedDocument.Settings):
        name = 'integration_events'


class DelayedEventDocument(IntegrationEventDocument):
    delayed: int

    class Settings(BasedDocument.Settings):
        name = 'delayed_events'
