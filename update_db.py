from sqlalchemy_utils import drop_database

from app import config
from app.database.manage import update_database

drop_database(str(config.SQLALCHEMY_DATABASE_URI))

update_database()
