"""Test smart user input string matching."""
import pytest
from agiocli import utils


COURSES = [
    {'pk': 17, 'name': 'EECS 280', 'semester': 'Spring', 'year': 2018},
    {'pk': 26, 'name': 'EECS 280', 'semester': 'Fall', 'year': 2018},
    {'pk': 32, 'name': 'EECS 280', 'semester': 'Winter', 'year': 2019},
    {'pk': 43, 'name': 'EECS 280', 'semester': 'Spring', 'year': 2019},
    {'pk': 50, 'name': 'EECS 280', 'semester': 'Fall', 'year': 2019},
    {'pk': 100, 'name': 'EECS 280', 'semester': 'Winter', 'year': 2021},
    {'pk': 111, 'name': 'EECS 280', 'semester': 'Spring', 'year': 2021},
    {'pk': 21, 'name': 'EECS 280 Diagnostic', 'semester': None, 'year': None},
    {'pk': 35, 'name': 'EECS 485', 'semester': 'Winter', 'year': 2019},
    {'pk': 46, 'name': 'EECS 485', 'semester': 'Fall', 'year': 2019},
    {'pk': 74, 'name': 'EECS 485', 'semester': 'Summer', 'year': 2020},
    {'pk': 85, 'name': 'EECS 485', 'semester': 'Fall', 'year': 2020},
    {'pk': 109, 'name': 'EECS 485', 'semester': 'Spring', 'year': 2021}
]


def test_find_course_returns_object():
    """Verify find_course() return an unmodified course object."""
    course = utils.find_course("EECS 485 Spring 2021", COURSES)
    assert course == {
        'pk': 109, 'name': 'EECS 485', 'semester': 'Spring', 'year': 2021
    }


@pytest.mark.parametrize(
    "user_input, expected_course_pk",
    [
        ("EECS 485 Spring 2021", 109),
        ("EECS 485 Spring 21", 109),
        ("EECS 485 sp 21", 109),
        ("485 sp 21", 109),
        ("EECS 280 Spring 2021", 111),
        ("EECS 280 Spring 21", 111),
        ("EECS 280 sp 21", 111),
        ("280 sp 21", 111),
    ]
)
def test_find_course_input_patterns(user_input, expected_course_pk):
    """Many supported input patterns."""
    course = utils.find_course(user_input, COURSES)
    assert course["pk"] == expected_course_pk
