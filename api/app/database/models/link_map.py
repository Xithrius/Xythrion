from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import String

from app.database.base import Base


class LinkMapModel(Base):
    __tablename__ = "link_maps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    server_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    from_match: Mapped[str] = mapped_column(String)
    to_match: Mapped[str] = mapped_column(String)
