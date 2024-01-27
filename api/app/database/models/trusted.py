import uuid
from datetime import datetime

from sqlalchemy import UUID, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.base import Base


class TrustedModel(Base):
    __tablename__ = "trusted"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    at: Mapped[datetime] = mapped_column(DateTime, default=now())
