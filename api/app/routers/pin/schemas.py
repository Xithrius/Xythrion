from datetime import datetime

from pydantic import BaseModel


class PinBase(BaseModel):
    server_id: int
    channel_id: int
    message_id: int


class Pin(PinBase):
    user_id: int
    created_at: datetime


class PinCreate(PinBase):
    user_id: int
