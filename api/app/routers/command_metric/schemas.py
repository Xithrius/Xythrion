from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommandMetricCreate(BaseModel):
    command_name: str
    successfully_completed: bool


class CommandMetricUpdate(BaseModel):
    pass


class CommandMetric(BaseModel):
    id: UUID
    used_at: datetime
    command_name: str
    successfully_completed: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
