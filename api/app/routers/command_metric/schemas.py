from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommandMetricCreate(BaseModel):
    command_name: str
    successfully_completed: bool


class CommandMetric(BaseModel):
    id: int
    used_at: datetime
    command_name: str
    successfully_completed: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
