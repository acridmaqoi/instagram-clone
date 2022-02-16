from app.database.core import Base
from app.models import BaseModel
from sqlalchemy import Column, ForeignKey, Integer


class Follow(Base):
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("instagram_user.id"))
    to_user_id = Column(Integer, ForeignKey("instagram_user.id"))
