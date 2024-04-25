from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, add_user_info
from studsched.app.db.models import models
from datetime import datetime


def test_get_subjects_empty(db_session: Session, user: models.User):
    res = get_subjects(db_session, user.id)
    assert res == []


def test_get_subjects(filled_db: Session, user: models.User):
    res = get_subjects(filled_db, user_id=user.id)
    assert len(res) == 1


def test_add_user_info(empty_db: Session):
    user = models.User(
        first_name="Bob",
        last_name="Rob",
        email="bob@rob.com",
        last_login=datetime.fromtimestamp(0),
    )
    user_info = models.UserInfo(
        user=user,
        courses=[models.CourseCreate(name="zprp", code="103A-INSZI-ISP-ZPRP")],
    )

    add_user_info(empty_db, user_info)
    subjects = get_subjects(empty_db, user_id=user.id)

    assert len(subjects) == 1
