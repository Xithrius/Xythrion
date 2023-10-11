from pydantic import BaseModel


class CommandMetric(BaseModel):
    command_name: str
    successfully_completed: bool
