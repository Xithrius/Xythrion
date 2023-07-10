from datetime import datetime

from ormar import (
    BigInteger,
    Model,
    Text,
    DateTime
)

from api.database.db import ParentMeta


class LinkMap(Model):
    class Meta(ParentMeta):
        tablename = "link_map"

    id: int = BigInteger(primary_key=True)
    created_at: datetime = DateTime(nullable=True)
    sid: int = BigInteger()
    uid: int = BigInteger()
    from_match: str = Text()
    to_match: str = Text()
