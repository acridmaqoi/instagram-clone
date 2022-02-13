import re

from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer

from ..database import Base


class Record(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    time_updated = Column(DateTime, server_onupdate=func.now())
