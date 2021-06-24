"""Test smart user input string matching."""
import pytest
from agiocli import utils


COURSES = [
    {"pk": 1, "name": "EECS 280", "semester": "Fall", "year": 2016},
    {"pk": 2, "name": "EECS 280", "semester": "Winter", "year": 2017},
    {"pk": 3, "name": "EECS 490", "semester": "Fall", "year": 2017},
    {"pk": 4, "name": "EECS 280", "semester": "Spring", "year": 2017},
    {"pk": 5, "name": "ENGR 101 F17", "semester": None, "year": None},
    {"pk": 7, "name": "EECS 280", "semester": "Fall", "year": 2017},
    {"pk": 8, "name": "EECS 485", "semester": "Fall", "year": 2017},
    {"pk": 9, "name": "AERO 552 Practice", "semester": None, "year": None},
    {"pk": 10, "name": "EECS 481", "semester": "Winter", "year": 2018},
    {"pk": 12, "name": "EECS 280", "semester": "Winter", "year": 2018},
    {"pk": 14, "name": "ENGR 101", "semester": "Winter", "year": 2018},
    {"pk": 15, "name": "EECS 485", "semester": "Winter", "year": 2018},
    {"pk": 16, "name": "EECS 398: System Design of a Search Engine",
        "semester": "Winter", "year": 2019},
    {"pk": 17, "name": "EECS 280", "semester": "Spring", "year": 2018},
    {"pk": 18, "name": "EECS 370", "semester": "Spring", "year": 2018},
    {"pk": 19, "name": "Demo EECS 280 F17", "semester": None, "year": None},
    {"pk": 20, "name": "Demo Course", "semester": None, "year": None},
    {"pk": 21, "name": "EECS 280 Diagnostic", "semester": None, "year": None},
    {"pk": 22, "name": "EECS 183", "semester": "Fall", "year": 2018},
    {"pk": 23, "name": "Copy of EECS 280 SP 2018",
        "semester": None, "year": None},
    {"pk": 25, "name": "EECS 490", "semester": "Fall", "year": 2018},
    {"pk": 26, "name": "EECS 280", "semester": "Fall", "year": 2018},
    {"pk": 27, "name": "EECS 285", "semester": "Fall", "year": 2018},
    {"pk": 29, "name": "EECS 485", "semester": "Fall", "year": 2018},
    {"pk": 30, "name": "ENGR 101", "semester": "Fall", "year": 2018},
    {"pk": 31, "name": "EECS 498-001 (Data Mining)",
        "semester": "Fall", "year": 2018},
    {"pk": 32, "name": "EECS 280", "semester": "Winter", "year": 2019},
    {"pk": 33, "name": "EECS 183 All Projects",
        "semester": None, "year": None},
    {"pk": 34, "name": "EECS 183", "semester": "Winter", "year": 2019},
    {"pk": 35, "name": "EECS 485", "semester": "Winter", "year": 2019},
    {"pk": 36, "name": "ENGR 101", "semester": "Winter", "year": 2019},
    {"pk": 37, "name": "EECS 481", "semester": "Winter", "year": 2019},
    {"pk": 38, "name": "EECS 598-008 Advanced Data Mining",
        "semester": "Winter", "year": 2019},
    {"pk": 40, "name": "EECS 483", "semester": "Winter", "year": 2019},
    {"pk": 41, "name": "EECS 493", "semester": "Winter", "year": 2019},
    {"pk": 42, "name": "EECS 370", "semester": "Fall", "year": 2019},
    {"pk": 43, "name": "EECS 280", "semester": "Spring", "year": 2019},
    {"pk": 44, "name": "EECS 490", "semester": "Fall", "year": 2019},
    {"pk": 45, "name": "EECS 285", "semester": "Fall", "year": 2019},
    {"pk": 46, "name": "EECS 485", "semester": "Fall", "year": 2019},
    {"pk": 47, "name": "EECS 183", "semester": "Fall", "year": 2019},
    {"pk": 48, "name": "ENGR 151", "semester": "Fall", "year": 2019},
    {"pk": 49, "name": "MSci Computer Science",
        "semester": "Summer", "year": 2020},
    {"pk": 50, "name": "EECS 280", "semester": "Fall", "year": 2019},
    {"pk": 51, "name": "EECS 481", "semester": "Fall", "year": 2019},
    {"pk": 52, "name": "ENGR 101", "semester": "Fall", "year": 2019},
    {"pk": 53, "name": "EECS 398: System Design of a Search Engine",
        "semester": "Fall", "year": 2019},
    {"pk": 54, "name": "EECS 484", "semester": "Fall", "year": 2019},
    {"pk": 55, "name": "EECS 183", "semester": "Winter", "year": 2020},
    {"pk": 56, "name": "EECS 280", "semester": "Winter", "year": 2020},
    {"pk": 57, "name": "ENGR 101", "semester": "Winter", "year": 2020},
    {"pk": 58, "name": "EECS 481", "semester": "Winter", "year": 2020},
    {"pk": 59, "name": "EECS 485", "semester": "Winter", "year": 2020},
    {"pk": 60, "name": "EECS 370", "semester": "Winter", "year": 2020},
    {"pk": 61, "name": "CIS 350", "semester": "Winter", "year": 2020},
    {"pk": 62, "name": "EECS 476", "semester": "Winter", "year": 2020},
    {"pk": 63, "name": "EECS 484", "semester": "Winter", "year": 2020},
    {"pk": 64, "name": "EECS 483", "semester": "Winter", "year": 2020},
    {"pk": 67, "name": "EECS 490 (Omar)", "semester": "Winter", "year": 2020},
    {"pk": 68, "name": "EECS 481", "semester": "Spring", "year": 2020},
    {"pk": 69, "name": "EECS 370", "semester": "Spring", "year": 2020},
    {"pk": 70, "name": "EECS 280", "semester": "Spring", "year": 2020},
    {"pk": 71, "name": "EECS 484", "semester": "Spring", "year": 2020},
    {"pk": 74, "name": "EECS 485", "semester": "Summer", "year": 2020},
    {"pk": 75, "name": "EECS 280 - INCOMPLETES",
        "semester": "Winter", "year": 2020},
    {"pk": 76, "name": "EECS 484 (copied from F19)",
        "semester": "Fall", "year": 2020},
    {"pk": 77, "name": "EECS 484 Fall 2020 (official)",
        "semester": "Fall", "year": 2020},
    {"pk": 78, "name": "EECS 183", "semester": "Fall", "year": 2020},
    {"pk": 79, "name": "EECS 498/598 Deep Learning for Computer Vision",
        "semester": "Fall", "year": 2020},
    {"pk": 80, "name": "EECS 280", "semester": "Fall", "year": 2020},
    {"pk": 81, "name": "CIS 350", "semester": "Fall", "year": 2020},
    {"pk": 82, "name": "EECS 481", "semester": "Fall", "year": 2020},
    {"pk": 83, "name": "EECS 370", "semester": "Fall", "year": 2020},
    {"pk": 85, "name": "EECS 485", "semester": "Fall", "year": 2020},
    {"pk": 86, "name": "EECS 285", "semester": "Fall", "year": 2020},
    {"pk": 87, "name": "ENGR 101", "semester": "Fall", "year": 2020},
    {"pk": 88, "name": "Research and Development Autograder",
        "semester": "Fall", "year": 2020},
    {"pk": 89, "name": "ENGR 151", "semester": "Fall", "year": 2020},
    {"pk": 90, "name": "EECS 398-001", "semester": "Winter", "year": 2021},
    {"pk": 91, "name": "EECS 183 - Elevators Development OUTDATED",
        "semester": "Fall", "year": 2020},
    {"pk": 93, "name": "ENGR 101", "semester": "Winter", "year": 2021},
    {"pk": 94, "name": "EECS 485", "semester": "Winter", "year": 2021},
    {"pk": 95, "name": "EECS 440: System Design of a Search Engine",
        "semester": "Winter", "year": 2021},
    {"pk": 96, "name": "EECS 481", "semester": "Winter", "year": 2021},
    {"pk": 97, "name": "EECS 484 Winter 2021",
        "semester": "Winter", "year": 2021},
    {"pk": 98, "name": "EECS 476", "semester": "Winter", "year": 2021},
    {"pk": 99, "name": "EECS 183", "semester": "Winter", "year": 2021},
    {"pk": 100, "name": "EECS 280", "semester": "Winter", "year": 2021},
    {"pk": 101, "name": "EECS 370", "semester": "Winter", "year": 2021},
    {"pk": 102, "name": "EECS 590", "semester": "Winter", "year": 2021},
    {"pk": 106, "name": "EECS 442 Computer Vision Winter 2021",
        "semester": "Winter", "year": 2021},
    {"pk": 107, "name": "EECS 483", "semester": "Winter", "year": 2021},
    {"pk": 108, "name": "CIS 350", "semester": "Winter", "year": 2021},
    {"pk": 109, "name": "EECS 485", "semester": "Spring", "year": 2021},
    {"pk": 110, "name": "EECS 484 Spring 2021",
        "semester": "Spring", "year": 2021},
    {"pk": 111, "name": "EECS 280", "semester": "Spring", "year": 2021},
    {"pk": 112, "name": "EECS 370", "semester": "Spring", "year": 2021},
    {"pk": 113, "name": "EECS 370 - Make up",
        "semester": "Spring", "year": 2021},
    {"pk": 126, "name": "ENGR 101", "semester": "Fall", "year": 2021}
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
    "user_input, expected_course_pk",
    [
        ("EECS 598 Winter 2019", 38),
        ("EECS 398 Fall 2019", 53),
        ("EECS 490 Winter 2020", 67),
        # ("EECS 484 Fall 2020", 77)
        # Above won't match because there is a duplicate
        ("EECS 498 Fall 2020", 79),  # This won't match on EECS 598
        ("EECS 398 Winter 2021", 90),
        ("EECS 598 wn 19", 38),
        ("EECS 398 fa 19", 53),
        ("EECS 490 wn 20", 67),
        # ("EECS 484 f 20", 77),
        # Above won't match because there is a duplicate
        ("EECS 498 f 20", 79),  # This won't match on EECS 598
        ("EECS 398 w 21", 90),
        ("598 wn 19", 38),
        ("398 fa 19", 53),
        ("490 wn 20", 67),
        # ("484 f 20", 77),
        # Above won't match because there is a duplicate
        ("498 f 20", 79),  # This won't match on EECS 598
        ("398 w 21", 90),
        ("598wn19", 38),
        ("398fa19", 53),
        ("490wn20", 67),
        # ("484f20", 77),
        # Above won't match because there is a duplicate
        ("498f20", 79),  # This won't match on EECS 598
        ("398w21", 90),
    ]
)
def test_course_match_strange_name(user_input, expected_course_pk):
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
