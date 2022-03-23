def test_create(db_session, post, user):
    from instagram.like.models import Like
    from instagram.like.service import create

    like = create(db=db_session, current_user=user, current_post=post)
    assert like
