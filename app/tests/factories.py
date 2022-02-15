from typing import Sequence

from app.auth.models import InstagramUser, hash_password
from factory import Sequence
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
