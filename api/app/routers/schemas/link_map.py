from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LinkMapChannelCreate(BaseModel):
    server_id: int
    input_channel_id: int
    output_channel_id: int


class LinkMapChannelUpdate(BaseModel):
    pass


class LinkMapChannel(BaseModel):
    id: UUID
    server_id: int
    input_channel_id: int
    output_channel_id: int
    created_at: datetime


class LinkMapConverterCreate(BaseModel):
    channel_map_id: int
    from_link: str
    to_link: str | None = None
    xpath: str | None = None


class LinkMapConverterUpdate(BaseModel):
    pass


class LinkMapConverter(BaseModel):
    id: UUID
    channel_map_id: int
    created_at: datetime
    from_link: str
    to_link: str | None = None
    xpath: str | None = None


class LinkMapChannelConverters(LinkMapChannel):
    link_maps: list[LinkMapConverter]
