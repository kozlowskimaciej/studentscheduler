from studsched.app.api.authorization import parse_usos_data
from studsched.app.db.models import models

from datetime import datetime
from freezegun import freeze_time
from hypothesis import given, strategies as st


user_strategy = st.fixed_dictionaries(
    {
        "first_name": st.text(),
        "last_name": st.text(),
        "middle_names": st.one_of(st.none(), st.text()),
        "email": st.emails(),
        "student_number": st.text(),
    }
)

course_edition_strategy = st.fixed_dictionaries(
    {
        "course_id": st.text(),
        "course_name": st.fixed_dictionaries(
            {
                "pl": st.text(),
                "en": st.text(),
            }
        ),
    }
)

courses_strategy = st.fixed_dictionaries(
    {
        "course_editions": st.dictionaries(
            keys=st.text(),
            values=st.lists(course_edition_strategy, max_size=5),
        )
    }
)


@freeze_time("1970-01-01")
@given(usos_user=user_strategy, usos_courses=courses_strategy)
def test_parse_usos_data(usos_user, usos_courses):

    user = models.UserCreate(
        index=usos_user["student_number"],
        first_name=usos_user["first_name"],
        middle_names=usos_user["middle_names"],
        last_name=usos_user["last_name"],
        email=usos_user["email"],
        last_login=datetime.now(),
    )

    courses = [
        models.CourseCreate(
            name=course_data["course_name"]["pl"],
            code=course_data["course_id"],
        )
        for courses in usos_courses["course_editions"].values()
        for course_data in courses
    ]

    user_info: models.UserInfo = parse_usos_data(usos_user, usos_courses)

    assert user_info.user == user
    assert user_info.courses == courses
