from webbrowser import get

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..internal.database import get_db
from ..internal.models.post import Post
from ..internal.models.post_image import PostImage
from ..schemas.post import Post as PostCreate

router = APIRouter()


@router.post("")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return Post.create(
        db=db,
        inital_caption=post.inital_caption,
        image_urls=[PostImage(image_url=image_url) for image_url in post.image_urls],
    )


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return Post.get_by_id(db=db, id=post_id)


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    Post.delete_by_id(db=db, id=post_id)
    return {"ok": True}
