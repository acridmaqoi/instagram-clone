from app.schemas.post import PostCreate, PostResponse
from sqlalchemy.orm import Session

from ..models.post import Post
from . import record_crud


def get_post_by_id(db: Session, post_id: int):
    return record_crud.get_record_by_id(db=db, id=post_id, model=Post)


def create_post(db: Session, post: PostCreate, user_id: int):
    return record_crud.write_record(db=db, record=Post(**post.dict(), user_id=user_id))


def delete_post(db: Session, post_id: int):
    return record_crud.delete_record_by_id(db=db, id=post_id, model=Post)
