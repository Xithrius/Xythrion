from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import String

from app.database.base import Base


class DeepRockGalacticBuildModel(Base):
    __tablename__ = "drg_builds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    user_id: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now())

    dwarf_class: Mapped[str] = mapped_column(String)
    build: Mapped[str] = mapped_column(String)
    overclock: Mapped[str] = mapped_column(String)
