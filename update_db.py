from sqlalchemy_utils import drop_database

from instagram import config
from instagram.database.manage import init_database, update_database

update_database()
