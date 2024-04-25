from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, add_user_info
from studsched.app.db.models import models
from datetime import datetime
import pytest


@pytest.mark.usefixtures("db_session")
def test_get_subjects_empty(user: models.User):
    res = get_subjects(user)
    assert res == []


@pytest.mark.usefixtures("filled_db")
def test_get_subjects(user: models.User):
    res = get_subjects(user)
    assert len(res) == 1


def test_add_user_info(empty_db: Session):
    user = models.UserCreate(
        first_name="Bob",
        last_name="Rob",
        email="bob@rob.com",
        last_login=datetime.fromtimestamp(0),
    )
    course = models.CourseCreate(name="zprp", code="103A-INSZI-ISP-ZPRP")
    user_info = models.UserInfo(
        user=user,
        courses=[course],
    )

    db_user = add_user_info(empty_db, user_info)
    subjects = get_subjects(db_user)

    assert len(subjects) == 1
