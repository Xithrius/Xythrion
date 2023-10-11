from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.base import Base


class PinModel(Base):
    __tablename__ = "pins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    server_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    message: Mapped[str] = mapped_column(String)
