import re

from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer

from ..database import Base


class RecordNotFound(Exception):
    def __init__(self, record, col: str, val: str):
        self.detail = f"{record.__name__} with {col}={val} not found"


class RecordRelationNotFound(Exception):
    def __init__(self, orig):
        col, val, table = re.search(
            'Key \((.*)\)=\((\d)\).*table "(.*)"', orig
        ).groups()
        model = Record.model_lookup_by_table_name(table)

        self.orig = orig
        self.detail = f"{model.__name__} with {col}={val} does not exist"


class Record(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    time_updated = Column(DateTime, server_onupdate=func.now())

    @classmethod
    def model_lookup_by_table_name(cls, table_name):
        registry_instance = getattr(cls, "registry")
        for mapper_ in registry_instance.mappers:
            model = mapper_.class_
            model_class_name = model.__tablename__
            if model_class_name == table_name:
                return model

    @classmethod
    def create(cls, db: Session, **data):
        try:
            record = cls(**data)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except IntegrityError as e:
            if isinstance(e.orig, ForeignKeyViolation):
                raise RecordRelationNotFound(orig=e.orig.args[0])
            else:
                raise

    @classmethod
    def get_by_id(cls, db: Session, id: int):
        record = db.query(cls).filter(cls.id == id).one_or_none()
        if record is None:
            raise RecordNotFound(record=cls, col="id", val=id)
        return record

    @classmethod
    def get_all(cls, db: Session, filters: dict = {}):
        return db.query(cls).filter_by(**filters).all()

    @classmethod
    def update_by_id(cls, db: Session, id: int, **data):
        record = cls.get_by_id(db, id)
        try:
            for key, value in data.items():
                setattr(record, key, value)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except IntegrityError as e:
            if isinstance(e.orig, ForeignKeyViolation):
                raise RecordRelationNotFound(orig=e.orig.args[0])
            else:
                raise

    @classmethod
    def delete_by_id(cls, db: Session, id: int):
        record = cls.get_by_id(db=db, id=id)
        db.delete(record)
        db.commit()
