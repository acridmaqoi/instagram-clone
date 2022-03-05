from sqlalchemy_utils import drop_database

from instagram import config
from instagram.database.manage import update_database

drop_database(str(config.SQLALCHEMY_DATABASE_URI))

update_database()
