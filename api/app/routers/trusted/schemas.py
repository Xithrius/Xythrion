from datetime import datetime

from pydantic import BaseModel


class TrustedCreate(BaseModel):
    user_id: int


class Trusted(BaseModel):
    id: int
    user_id: int
    at: datetime
