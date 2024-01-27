import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.base import Base


class CommandMetricModel(Base):
    __tablename__ = "command_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    used_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    command_name: Mapped[str] = mapped_column(String)
    successfully_completed: Mapped[bool] = mapped_column(Boolean)
