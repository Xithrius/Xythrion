from datetime import datetime

from ormar import BigInteger, Boolean, DateTime, Integer, Model, Text

from app.database.db import ParentMeta


class CommandMetric(Model):
    class Meta(ParentMeta):
        tablename = "command_metrics"

    id: int = Integer(primary_key=True)
    command_name: str = Text()
    used_at: datetime = DateTime(default=datetime.now)
    successfully_completed: bool = Boolean()


class LinkMap(Model):
    class Meta(ParentMeta):
        tablename = "link_map"

    id: int = Integer(primary_key=True)
    sid: int = BigInteger()
    uid: int = BigInteger()
    created_at: datetime = DateTime(default=datetime.now)
    from_match: str = Text()
    to_match: str = Text()


class WebPath(Model):
    class Meta(ParentMeta):
        tablename = "web_map"

    id: int = Integer(primary_key=True)
    sid: int = BigInteger()
    uid: int = BigInteger()
    created_at: datetime = DateTime(default=datetime.now)
    matches: str = Text()
    xpath: str = Text()


class DeepRockGalacticBuild(Model):
    class Meta(ParentMeta):
        tablename = "drg_builds"

    id: int = Integer(primary_key=True)
    uid: int = BigInteger()
    created_at: datetime = DateTime(default=datetime.now)
    dwarf_class: str = Text()
    build: str = Text()
    overclock: str = Text(nullable=True)
