from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, add_user_info
from studsched.app.db.models import models
import pytest


@pytest.mark.usefixtures("db_with_user")
def test_get_subjects_empty(user: models.User):
    res = get_subjects(user)
    assert res == []


@pytest.mark.usefixtures("db_with_courses")
def test_get_subjects(user: models.User):
    res = get_subjects(user)
    assert len(res) == 1


def test_add_user_info(
    empty_db: Session,
    user: models.User,
    course: models.Course,
):
    user_info = models.UserInfo(
        user=user,
        courses=[course],
    )

    db_user = add_user_info(empty_db, user_info)
    subjects = get_subjects(db_user)

    assert len(subjects) == 1
