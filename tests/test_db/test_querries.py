from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects


def test_get_subjects_empty(db_session: Session):
    res = get_subjects(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_subjects(filled_db)
    assert len(res) == 1
