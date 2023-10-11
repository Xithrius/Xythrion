from datetime import datetime

from pydantic import BaseModel


class WebMapCreate(BaseModel):
    server_id: int
    user_id: int
    matches: str
    xpath: str


class WebMap(BaseModel):
    id: int
    server_id: int
    user_id: int
    created_at: datetime
    matches: str
    xpath: str
