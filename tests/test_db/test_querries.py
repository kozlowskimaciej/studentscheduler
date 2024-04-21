from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, add_user_info
from studsched.app.db.models import models


def test_get_subjects_empty(db_session: Session):
    res = get_subjects(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_subjects(filled_db)
    assert len(res) == 1


def test_add_user_info(db_session: Session):
    user_info = models.UserInfo(
        user=models.UserPublic(
            id=7,
            first_name="Bob",
            last_name="Rob",
        ),
        courses=[models.CoursePublic(id=2, name="zprp")],
    )

    add_user_info(db_session, user_info)
    subjects = get_subjects(db_session)

    assert len(subjects) == 1
