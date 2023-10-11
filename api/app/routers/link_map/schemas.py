from datetime import datetime

from pydantic import BaseModel


class LinkMapCreate(BaseModel):
    server_id: int
    user_id: int
    created_at: datetime
    from_match: str
    to_match: str


class LinkMap(BaseModel):
    id: int
    server_id: int
    user_id: int
    created_at: datetime
    from_match: str
    to_match: str
