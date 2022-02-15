from app import config
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from .core import Base


def get_tables():
    """Get all the tables in the application"""
    tables = []
    for _, table in Base.metadata.tables.items():
        tables.append(table)
    return tables


def init_database(engine):
    """Initializes the database"""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))

    # create the core schema
    schema_name = "instagram_core"
    if not engine.dialect.has_schema(engine, schema_name):
        with engine.connect() as connection:
            connection.execute(CreateSchema(schema_name))

    Base.metadata.create_all(engine, tables=get_tables())

    # TODO additional initalization here as needed
