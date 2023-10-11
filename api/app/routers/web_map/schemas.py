from pydantic import BaseModel


class WebMap(BaseModel):
    server_id: int
    user_id: int
    matches: str
    xpath: str
