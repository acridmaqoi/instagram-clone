from instagram.auth.models import UserRead
from instagram.database.core import Base, SessionLocal
from instagram.models import InstagramBase
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, delete, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class Like(Base):
    id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer, ForeignKey("likeable_entity.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("instagram_user.id"), nullable=False)

    user = relationship("InstagramUser", back_populates="likes", uselist=False)
    entity = relationship("LikeableEntity", back_populates="likes", uselist=False)
