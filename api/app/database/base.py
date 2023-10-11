from sqlalchemy.orm import DeclarativeBase

from .meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
