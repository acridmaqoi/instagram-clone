from typing import List

from app.auth.models import InstagramUser
from app.friendship.models import Follow
from app.tests.conftest import get_user_authenticated_client
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_follow_user(client: TestClient, instagram_users: List[InstagramUser]):
    user_1 = instagram_users[0]
    user_2 = instagram_users[1]

    follow_res = client.post(
        f"/friendships/{user_2.id}/follow",
        headers={"Authorization": f"Bearer {user_1.token}"},
    )
    assert follow_res.status_code == status.HTTP_200_OK

    # TODO just assert on database: endpoints are already tested in auth
    # check user 1 is following
    user_res = client.get(
        f"/auth/current", headers={"Authorization": f"Bearer {user_1.token}"}
    )
    assert user_res.status_code == status.HTTP_200_OK
    assert user_res.json()["following_count"] == 1

    # check user 2 has a follower
    user_res = client.get(
        f"/auth/current", headers={"Authorization": f"Bearer {user_2.token}"}
    )
    assert user_res.status_code == status.HTTP_200_OK
    assert user_res.json()["followers_count"] == 1


def test_unfollow_user(client: TestClient, follow: Follow):
    unfollow_res = client.post(
        f"/friendships/{follow.to_user_id}/unfollow",
        headers={"Authorization": f"Bearer {follow.from_user.token}"},
    )

    assert unfollow_res.status_code == status.HTTP_200_OK
