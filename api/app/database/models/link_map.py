from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import UUID, BigInteger, CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.database.base import Base


class LinkMapChannelModel(Base):
    __tablename__ = "link_map_channels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    server_id = mapped_column(BigInteger)
    input_channel_id = mapped_column(BigInteger)
    output_channel_id = mapped_column(BigInteger)

    converters: Mapped[list[LinkMapConverterModel]] = relationship(
        "LinkMapConverter",
        secondary="channel_converter_association",
        back_populates="link_map_converters",
        lazy="joined",
    )


class LinkMapConverterModel(Base):
    __tablename__ = "link_map_converters"

    __table_args__ = (
        CheckConstraint(
            "((to_link IS NOT NULL AND xpath IS NULL) OR (to_link IS NULL AND xpath IS NOT NULL))",
            name="check_xor_constraint",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    from_link: Mapped[str] = mapped_column(String)
    to_link: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    xpath: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

    channels: Mapped[list[LinkMapChannelModel]] = relationship(
        "LinkMapChannels",
        secondary="channel_converter_association",
        back_populates="link_map_channels",
        lazy="joined",
    )


class LinkMapChannelConverterAssociationModel(Base):
    __tablename__ = "channel_converter_association"

    channel_id = mapped_column(
        UUID,
        ForeignKey("link_map_channels.id", ondelete="CASCADE"),
        primary_key=True,
    )
    converter_id = mapped_column(
        UUID,
        ForeignKey("link_map_converters.id", ondelete="CASCADE"),
        primary_key=True,
    )
