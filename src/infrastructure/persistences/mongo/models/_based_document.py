from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Granularity, TimeSeriesConfig, Indexed
from pydantic import Field


class BasedDocument(Document):
    id: Indexed(UUID) = Field(default=uuid4, alias="_id")
    _created: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    _updated: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    _deleted: bool = False

    class Settings:
        _created_timeseries = TimeSeriesConfig(
            time_field="created",  # Required
            granularity=Granularity.hours,  # Optional
            expire_after_seconds=2  # Optional
        )

        _updated_timeseries = TimeSeriesConfig(
            time_field="updated",  # Required
            granularity=Granularity.hours,  # Optional
            expire_after_seconds=2  # Optional
        )
