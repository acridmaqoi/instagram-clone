import json

import pytest
from app.auth.models import InstagramUser
from app.post.models import Comment, Like, Post
from app.tests.conftest import get_user_authenticated_client
from fastapi import status
from fastapi.testclient import TestClient


def test_create(db_session, instagram_user: InstagramUser):
    user_client = get_user_authenticated_client(
        db_session=db_session, user=instagram_user
    )

    post_caption = "test post"
    create_res = user_client.post("/posts", json={"caption": post_caption})
    assert create_res.status_code == status.HTTP_200_OK

    post_id = create_res.json()["id"]
    get_res = user_client.get(f"/posts/{post_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["id"] == post_id
    assert get_res.json()["caption"] == post_caption


# TODO paramertize: test against another user
def test_delete(db_session, post: Post):
    user_client = get_user_authenticated_client(db_session=db_session, user=post.user)

    delete_res = user_client.delete(f"/posts/{post.id}")
    assert delete_res.status_code == status.HTTP_200_OK

    get_res = user_client.get(f"/posts/{post.id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_like(db_session, post: Post, instagram_user: InstagramUser):
    user_client = get_user_authenticated_client(
        db_session=db_session, user=instagram_user
    )

    like_res = user_client.post(f"/posts/{post.id}/likes")
    assert like_res.status_code == status.HTTP_200_OK

    # TODO assert like is in GET response


def test_dislike(db_session, like: Like, instagram_user: InstagramUser):
    user_client = get_user_authenticated_client(
        db_session=db_session, user=instagram_user
    )

    dislike_res = user_client.delete(f"/posts/{like.entity.id}/likes")
    assert dislike_res.status_code == status.HTTP_200_OK


def test_add_comment(db_session, post: Post, instagram_user: InstagramUser):
    user_client = get_user_authenticated_client(
        db_session=db_session, user=instagram_user
    )

    comment = "test comment"
    comment_res = user_client.post(
        f"/posts/{post.id}/comments", json={"comment": comment}
    )
    assert comment_res.status_code == status.HTTP_200_OK

    # TODO assert GET


def test_uncomment(db_session, comment: Comment):
    user_client = get_user_authenticated_client(
        db_session=db_session, user=comment.user
    )

    uncomment_res = user_client.delete(
        f"/posts/{comment.post.id}/comments/{comment.id}"
    )
    assert uncomment_res.status_code == status.HTTP_200_OK

    # TODO assert GET
