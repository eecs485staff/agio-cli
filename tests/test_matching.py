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


def test_course_match_returns_object():
    """Verify match is an unmodified course object."""
    course = utils.course_match("EECS 485 Spring 2021", COURSES)
    assert course == {
        'pk': 109, 'name': 'EECS 485', 'semester': 'Spring', 'year': 2021
    }


@pytest.mark.parametrize(
    "user_input, expected_course_pk",
    [
        ("EECS 280 Spring 2021", 111),
        ("EECS 485 Spring 2021", 109),
        ("EECS 280 Spring 21", 111),
        ("EECS 485 Spring 21", 109),
        ("EECS 280 sp 21", 111),
        ("EECS 485 sp 21", 109),
        ("280 sp 21", 111),
        ("485 sp 21", 109),
        ("eecs280sp21", 111),
        ("eecs485sp21", 109),
    ]
)
def test_course_match_input_patterns(user_input, expected_course_pk):
    """Many supported input patterns."""
    course = utils.course_match(user_input, COURSES)
    assert course["pk"] == expected_course_pk


@pytest.mark.parametrize(
    "user_input",
    [
        ("EECS 280 Spring 2016"),
        ("EECS 485 Spring 2016"),
        ("EECS 280 Spring 16"),
        ("EECS 485 Spring 16"),
        ("EECS 280 sp 16"),
        ("EECS 485 sp 16"),
        ("280 sp 16"),
        ("485 sp 16"),
        ("eecs280sp16"),
        ("eecs485sp16"),
    ]
)
def test_course_match_bad_year(user_input):
    """Bad year in pattern."""
    course = utils.course_match(user_input, COURSES)
    assert course is None
