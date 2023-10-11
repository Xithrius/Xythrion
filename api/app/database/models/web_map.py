from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import String

from app.database.base import Base


class WebMapModel(Base):
    __tablename__ = "web_maps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    server_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

    matches: Mapped[str] = mapped_column(String)
    xpath: Mapped[str] = mapped_column(String)
