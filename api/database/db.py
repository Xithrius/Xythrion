import os

from databases import Database
from dotenv import load_dotenv
from ormar import ModelMeta
from sqlalchemy import MetaData

load_dotenv()

database = Database(os.environ["DB_URI"])
metadata = MetaData()


class ParentMeta(ModelMeta):
    """Base meta class for all Ormar models."""

    database = database
    metadata = metadata
