from os import getenv

from databases import Database
from dotenv import load_dotenv
from loguru import logger as log
from ormar import ModelMeta
from sqlalchemy import MetaData

load_dotenv()

postgres_host = getenv("POSTGRES_HOST", "localhost")
log.info(postgres_host)

database = Database(f"postgresql://xythrion:xythrion@{postgres_host}:5432/xythrion")
metadata = MetaData()


class ParentMeta(ModelMeta):
    """Base meta class for all Ormar models."""

    database = database
    metadata = metadata
