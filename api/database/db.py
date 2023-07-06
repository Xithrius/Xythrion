from os import environ

from databases import Database
from ormar import ModelMeta
from sqlalchemy import MetaData

database = Database(environ["DB_URI"])
metadata = MetaData()


class ParentMeta(ModelMeta):
    """Base meta class for all Ormar models."""

    database = database
    metadata = metadata
