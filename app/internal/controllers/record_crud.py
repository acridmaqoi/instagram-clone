import re
from typing import Any, Type

from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from ..models.record import Record


def model_lookup_by_table_name(table_name):
    registry_instance = getattr(Record, "registry")
    for mapper_ in registry_instance.mappers:
        model = mapper_.class_
        model_class_name = model.__tablename__
        if model_class_name == table_name:
            return model.__name__


class RecordNotFound(NoResultFound):
    def __init__(self, record, col, val):
        self.detail = f"{record.__name__} with {col}={val} not found"


class RecordRelationNotFound(ForeignKeyViolation):
    def __init__(self, orig):
        col, val, table = re.search(
            'Key \((.*)\)=\((\d)\).*table "(.*)"', orig  # type: ignore
        ).groups()  # type: ignore
        model = model_lookup_by_table_name(table)
        self.detail = f"{model} with {col}={val} does not exist"


class RecordAlreadyExists(UniqueViolation):
    def __init__(self, model, orig, *args, **kwargs):
        col, val = re.search("Key \((.*)\)=\((.*)\).*", orig).groups()  # type: ignore
        self.detail = f"{model} with {col}={val} already exists"


def write_record(db: Session, record: Record):
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolation):
            raise RecordRelationNotFound(orig=e.orig.args[0])
        elif isinstance(e.orig, UniqueViolation):
            raise RecordAlreadyExists(
                model=record.__class__.__name__, orig=e.orig.args[0]
            )
        else:
            raise


def get_record_by_id(db: Session, id: int, model: Type[Record]):
    record = db.query(model).filter_by(id=id).one_or_none()
    if record is None:
        raise RecordNotFound(record=model, col="id", val=id)
    return record


def get_all(cls, db: Session, filters: dict = {}):
    return db.query(cls).filter_by(**filters).all()


def update_record_by_id(cls, db: Session, id: int, updated_record: Record) -> Record:
    record = cls.get_by_id(db, id)
    try:
        for key, value in updated_record.__dict__:
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


def delete_record_by_id(db: Session, id: int, model: Type[Record]):
    record = get_record_by_id(db=db, id=id, model=model)
    db.delete(record)
    db.commit()
