from os import environ

from databases import Database
from sqlalchemy import MetaData

database = Database(environ["DB_URI"])
metadata = MetaData()
