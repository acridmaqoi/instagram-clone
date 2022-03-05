import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database
from starlette.config import environ

environ[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password@localhost:5433/instagram-test"

from instagram import config
from instagram.auth.models import InstagramUser
from instagram.auth.service import get_current_user
from instagram.database.core import engine
from instagram.database.manage import init_database
from sqlalchemy.orm import sessionmaker

from .database import Session
from .factories import (
    CommentFactory,
    FollowFactory,
    InstagramUserFactory,
    LikeFactory,
    PostFactory,
)


def get_user_authenticated_client(user: InstagramUser, db_session):
    from instagram.database.core import get_db
    from instagram.main import api

    api.dependency_overrides[get_db] = lambda: db_session
    api.dependency_overrides[get_current_user] = lambda: user

    return TestClient(api)


@pytest.fixture(scope="session")
def db():
    init_database(engine)
    yield
    drop_database(str(config.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="function", autouse=True)
def db_session(db):
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture(scope="function")
def client(db_session):
    from instagram.database.core import get_db
    from instagram.main import api

    api.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(api)


# Factories...


@pytest.fixture
def instagram_user(db_session):
    return InstagramUserFactory()


@pytest.fixture
def instagram_users(db_session):
    return [InstagramUserFactory(), InstagramUserFactory()]


@pytest.fixture
def post(db_session):
    return PostFactory()


@pytest.fixture
def like(db_session):
    return LikeFactory()


@pytest.fixture
def comment(db_session):
    return CommentFactory()


@pytest.fixture
def follow(db_session):
    return FollowFactory()
