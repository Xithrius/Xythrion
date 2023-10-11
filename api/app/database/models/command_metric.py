from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import String

from app.database.base import Base


class CommandMetricModel(Base):
    __tablename__ = "command_metrics"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    used_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    command_name: Mapped[str] = mapped_column(String)
    successfully_completed: Mapped[bool] = mapped_column(Boolean)
