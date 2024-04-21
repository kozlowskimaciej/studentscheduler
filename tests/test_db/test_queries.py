from sqlmodel import Session
from studsched.app.db.queries.queries import get_courses


def test_get_subjects_empty(db_session: Session):
    res = get_courses(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_courses(filled_db)
    assert len(res) == 1
