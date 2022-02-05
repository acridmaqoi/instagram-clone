from app.internal.database import Base, engine
from app.internal.models import post, post_image, record, user

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
