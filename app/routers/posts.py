from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..internal.database import get_db
from ..internal.models.post import Post
from ..internal.models.post_image import PostImage
from ..internal.models.user import User
from ..schemas.post import Post as PostCreate

router = APIRouter()


@router.post("")
def create_post(
    post: PostCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Post.create(
        db=db,
        user_id=user.id,
        inital_caption=post.inital_caption,
        image_urls=[PostImage(image_url=image_url) for image_url in post.image_urls],
    )


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return Post.get_by_id(db=db, id=post_id)


@router.delete("/{post_id}")
def delete_post(
    post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    post = Post.get_by_id(db=db, id=post_id)
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    db.delete(post)
    db.commit()
    return {"ok": True}
