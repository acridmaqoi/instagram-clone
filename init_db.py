from sqlalchemy_utils import drop_database

from instagram import config
from instagram.database.manage import init_database

try:
    drop_database(str(config.SQLALCHEMY_DATABASE_URI))
except:
    pass

init_database()
