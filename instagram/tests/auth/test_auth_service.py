import pytest
from instagram.profile.models import InstagramUser
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_register_user(db_session: Session, client: TestClient):
    register_response = client.post(
        "/auth/register",
        json={"username": "sammy", "email": "sammy@example.com", "password": "123"},
    )
    assert register_response.status_code == status.HTTP_200_OK
    assert register_response.json()["token"]

    # check user in db
    user = (
        db_session.query(InstagramUser)
        .filter(InstagramUser.username == "sammy")
        .one_or_none()
    )

    assert user
    assert user.email == "sammy@example.com"


def test_login_user(client: TestClient, instagram_user: InstagramUser):
    login_response = client.post(
        "/auth/login",
        json={
            "username": instagram_user.username,
            "email": instagram_user.email,
            "password": "password",
        },
    )
    assert login_response.status_code == status.HTTP_200_OK
    assert login_response.json()["token"]


def test_get_logged_in_user(client: TestClient, instagram_user: InstagramUser):
    user_response = client.get(
        "/auth/current", headers={"Authorization": f"Bearer {instagram_user.token}"}
    )
    assert user_response.status_code == status.HTTP_200_OK
    assert user_response.json()["username"] == instagram_user.username
    assert user_response.json()["email"] == instagram_user.email
