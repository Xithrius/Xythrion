from sqlalchemy.orm import DeclarativeBase, declared_attr

from .meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta


class MappedBase(DeclarativeBase):
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
