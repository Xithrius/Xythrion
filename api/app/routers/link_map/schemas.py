from datetime import datetime

from pydantic import BaseModel

class LinkMapChannelCreate(BaseModel):
    server_id: int
    input_channel_id: int
    output_channel_id: int


class LinkMapChannel(BaseModel):
    server_id: int
    input_channel_id: int
    output_channel_id: int
    created_at: datetime


class LinkMapCreate(BaseModel):
    channel_map_server_id: int
    from_link: str
    to_link: str


class LinkMap(BaseModel):
    id: int
    channel_map_server_id: int
    created_at: datetime
    from_link: str
    to_link: str
