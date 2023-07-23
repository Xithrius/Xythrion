from os import environ
from datetime import datetime

from databases import Database
from ormar import ModelMeta, Model, Integer, Text, DateTime, Boolean
from sqlalchemy import MetaData

database = Database(environ["DB_URI"])
metadata = MetaData()


class ParentMeta(ModelMeta):
    """Base meta class for all Ormar models."""

    database = database
    metadata = metadata

class CommandMetric(Model):
    class Meta(ParentMeta):
        tabelname = "command_metrics"

    id: int = Integer(primary_key=True)
    command_name: str = Text()
    used_at: datetime = DateTime()
    successfully_completed: bool = Boolean()
