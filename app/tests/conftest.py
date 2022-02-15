import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database
from starlette.config import environ

environ[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password@localhost:5433/instagram-test"

from app import config
from app.database.core import engine
from app.database.manage import init_database
from sqlalchemy.orm import sessionmaker

from .database import Session
from .factories import InstagramUserFactory


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
    from app.database.core import get_db
    from app.main import api

    api.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(api)


# Factories...


@pytest.fixture
def instagram_user(db_session):
    return InstagramUserFactory()
