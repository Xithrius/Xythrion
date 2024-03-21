from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import UUID, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.database.base import Base


class LinkMapChannelModel(Base):
    __tablename__ = "link_map_channels"

    # TODO: Change to UUID primary key, this implementation is not good

    server_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    input_channel_id: Mapped[int] = mapped_column(BigInteger)
    output_channel_id: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    link_maps: Mapped[list[LinkMapConverterModel]] = relationship(
        back_populates="channel_map",
        lazy="joined",
    )


class LinkMapConverterModel(Base):
    __tablename__ = "link_maps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    from_link: Mapped[str] = mapped_column(String)
    to_link: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    xpath: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    channel_map_server_id: Mapped[int] = mapped_column(
        ForeignKey("link_map_channels.server_id"),
    )

    channel_map: Mapped[LinkMapChannelModel] = relationship(
        back_populates="link_maps",
        lazy="joined",
    )
