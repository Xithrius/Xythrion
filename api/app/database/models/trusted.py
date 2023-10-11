from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.base import Base


class TrustedModel(Base):
    __tablename__ = "trusted"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    user_id = mapped_column(BigInteger, unique=True)
    at = mapped_column(DateTime, default=now)
