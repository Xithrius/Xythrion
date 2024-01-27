from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TrustedCreate(BaseModel):
    user_id: int


class Trusted(BaseModel):
    id: UUID
    user_id: int
    at: datetime
