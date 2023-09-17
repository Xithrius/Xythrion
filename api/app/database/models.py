from datetime import datetime

from ormar import BigInteger, Boolean, DateTime, Integer, Model, Text

from .db import ParentMeta


class CommandMetric(Model):
    class Meta(ParentMeta):
        tablename = "command_metrics"

    id = Integer(primary_key=True)
    command_name = Text()
    used_at = DateTime(default=datetime.now)
    successfully_completed = Boolean()


class LinkMap(Model):
    class Meta(ParentMeta):
        tablename = "link_maps"

    id = Integer(primary_key=True)
    server_id = BigInteger()
    user_id = BigInteger()
    created_at = DateTime(default=datetime.now)
    from_match = Text()
    to_match = Text()


class WebMap(Model):
    class Meta(ParentMeta):
        tablename = "web_maps"

    id = Integer(primary_key=True)
    server_id = BigInteger()
    user_id = BigInteger()
    created_at = DateTime(default=datetime.now)
    matches = Text()
    xpath = Text()


class DeepRockGalacticBuild(Model):
    class Meta(ParentMeta):
        tablename = "drg_builds"

    id = Integer(primary_key=True)
    user_id = BigInteger()
    created_at = DateTime(default=datetime.now)
    dwarf_class = Text()
    build = Text()
    overclock = Text(nullable=True)


class Trusted(Model):
    class Meta(ParentMeta):
        tablename = "trusted"

    id = Integer(primary_key=True)
    user_id = BigInteger(unique=True)
    at = DateTime(default=datetime.now)
