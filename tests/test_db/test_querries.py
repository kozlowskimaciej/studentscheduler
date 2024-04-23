from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, add_user_info
from studsched.app.db.models import models
from datetime import datetime


def test_get_subjects_empty(db_session: Session):
    res = get_subjects(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_subjects(filled_db)
    assert len(res) == 1


def test_add_user_info(db_session: Session):
    user_info = models.UserInfo(
        user=models.UserCreate(
            first_name="Bob",
            last_name="Rob",
            email="bob@rob.com",
            last_login=datetime.fromtimestamp(0),
        ),
        courses=[models.CourseCreate(name="zprp", code="103A-INSZI-ISP-ZPRP")],
    )

    add_user_info(db_session, user_info)
    subjects = get_subjects(db_session)

    assert len(subjects) == 1
