from datetime import datetime

from pydantic import BaseModel


class PinCreate(BaseModel):
    server_id: int
    channel_id: int
    message_id: int
    user_id: int


class Pin(BaseModel):
    server_id: int
    channel_id: int
    message_id: int
    user_id: int
    created_at: datetime
