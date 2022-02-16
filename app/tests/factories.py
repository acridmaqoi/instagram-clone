from typing import Sequence

from app import main  # noqa
from app.auth.models import InstagramUser, hash_password
from app.friendship.models import Follow
from app.post.models import Comment, Like, Post
from factory import Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText
from faker import Faker

from .database import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class InstagramUserFactory(BaseFactory):
    username = Faker().name()
    email = Sequence(lambda n: f"user{n}@example.com")
    username = FuzzyText()
    password = hash_password("password")

    class Meta:
        model = InstagramUser


class PostFactory(BaseFactory):

    caption = FuzzyText()
    user = SubFactory(InstagramUserFactory)

    class Meta:
        model = Post


class LikeFactory(BaseFactory):
    user = SubFactory(InstagramUserFactory)
    entity = SubFactory(PostFactory)  # TODO support comments

    class Meta:
        model = Like


class CommentFactory(BaseFactory):
    user = SubFactory(InstagramUserFactory)
    text = FuzzyText()
    post = SubFactory(PostFactory)

    class Meta:
        model = Comment


class FollowFactory(BaseFactory):
    from_user_id = SubFactory(InstagramUserFactory)
    to_user_id = SubFactory(InstagramUserFactory)

    class Meta:
        model = Follow
