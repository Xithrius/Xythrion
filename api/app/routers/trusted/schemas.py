from pydantic import BaseModel


class Trusted(BaseModel):
    user_id: int
