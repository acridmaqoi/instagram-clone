from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# class Comment(Record):
#    __tablename__ = "comment"
#
#    text = Column(String, nullable=False)
#    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
#    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#
#    post = relationship("Post", back_populates="comments", uselist=False)
