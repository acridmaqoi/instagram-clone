from instagram.database.core import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Save(Base):
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("instagram_user.id"), primary_key=True)

    user = relationship("InstagramUser", uselist=False, back_populates="saved_posts")
    post = relationship("Post", uselist=False, back_populates="saves")
