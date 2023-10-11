from datetime import datetime

from pydantic import BaseModel


class PinCreate(BaseModel):
    server_id: int
    user_id: int
    created_at: datetime
    message: str


class Pin(BaseModel):
    id: int
    server_id: int
    user_id: int
    created_at: datetime
    message: str
