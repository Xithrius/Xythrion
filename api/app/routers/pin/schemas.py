from datetime import datetime

from pydantic import BaseModel


class Pin(BaseModel):
    server_id: int
    user_id: int
    created_at: datetime
    message: str
