import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client():
    from app.main import api

    yield TestClient(api)
