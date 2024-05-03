from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ValidationError, validator
from pydantic.fields import FieldInfo


class LinkMapChannelCreate(BaseModel):
    server_id: int
    input_channel_id: int
    output_channel_id: int


class LinkMapChannelUpdate(BaseModel):
    pass


class LinkMapChannel(BaseModel):
    id: UUID
    created_at: datetime
    server_id: int
    input_channel_id: int
    output_channel_id: int


class LinkMapConverterCreate(BaseModel):
    from_link: str
    to_link: str | None = None
    xpath: str | None = None

    @classmethod
    @validator("to_link", "xpath")
    def only_one_of_to_link_or_xpath(cls, value: str | None, field: FieldInfo) -> str | None:
        if value and cls.model_fields[field.name].default:
            raise ValidationError("Only one of 'to_link' or 'xpath' can be provided, not both.")
        return value


class LinkMapConverterUpdate(BaseModel):
    pass


class LinkMapConverter(BaseModel):
    id: UUID
    created_at: datetime
    from_link: str
    to_link: str | None = None
    xpath: str | None = None


class LinkMapChannelConverters(LinkMapChannel):
    converters: list[LinkMapConverter]


class LinkMapConverterChannels(LinkMapConverter):
    channels: list[LinkMapChannel]
