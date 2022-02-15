from app import config, main  # noqa
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from .core import Base


def init_database(engine):
    """Initializes the database"""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))

    # create the core schema
    schema_name = "instagram_core"
    if not engine.dialect.has_schema(engine, schema_name):
        with engine.connect() as connection:
            connection.execute(CreateSchema(schema_name))

    schema_engine = engine.execution_options(
        schema_translate_map={
            None: "instagram_core",
        }
    )

    Base.metadata.create_all(schema_engine)

    # TODO additional initalization here as needed
