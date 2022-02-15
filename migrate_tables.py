from sqlalchemy_utils import drop_database

from app import config
from app.database.manage import init_database
from app.internal.database import engine

drop_database(str(config.SQLALCHEMY_DATABASE_URI))

init_database(engine)
