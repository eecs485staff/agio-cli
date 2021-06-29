"""System tests for courses subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import json
import textwrap
import click
import click.testing
import pytest
from agiocli.__main__ import main


# Unused arguments due to fixtures are endemic to pytest
# pylint: disable=unused-argument


@pytest.fixture(name="api_mock")
def api_requests_mock(requests_mock):
    """Mock Autograder API with hardcoded responses."""
    # User
    requests_mock.get(
        "https://autograder.io/api/users/current/",
        text=textwrap.dedent("""\
        {
            "pk": 5,
            "username": "awdeorio@umich.edu",
            "first_name": "Andrew",
            "last_name": "DeOrio",
            "email": "",
            "is_superuser": false
        }
        """)
    )
    # Course list
    requests_mock.get(
        "https://autograder.io/api/users/5/courses_is_admin_for/",
        text=json.dumps([
            {
                "pk": 111,
                "name": "EECS 280",
                "semester": "Spring",
                "year": 2021,
                "subtitle": "",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-05-03T01:12:28.049482Z"
            },
            {
                "pk": 109,
                "name": "EECS 485",
                "semester": "Spring",
                "year": 2021,
                "subtitle": "Web Systems",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-04-07T02:19:22.818992Z"
            },
            {
                "pk": 129,
                "name": "EECS 485",
                "semester": "Fall",
                "year": 2021,
                "subtitle": "Web Systems",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-06-23T13:54:07.942973Z"
            }
        ])
    )
    # Course detail
    requests_mock.get(
        "https://autograder.io/api/courses/109/",
        text=json.dumps({
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        })
    )


def test_courses_list(api_mock):
    """Verify agio courses list option.

    $ agio courses --list
    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "--list"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        [129]\tEECS 485 Fall 2021
        [109]\tEECS 485 Spring 2021
        [111]\tEECS 280 Spring 2021
    """)


def test_courses_empty(api_mock, mocker):
    """Verify courses subcommand no input.

    $ agio courses
    """
    # Mock user-selection menu, users selects course pk 109
    course_109 = {
        'pk': 109,
        'name': 'EECS 485',
        'semester': 'Spring',
        'year': 2021,
        'subtitle': 'Web Systems',
        'num_late_days': 0,
        'allowed_guest_domain': '@umich.edu',
        'last_modified': '2021-04-07T02:19:22.818992Z'
    }
    mocker.patch("pick.pick", return_value=(course_109, 1))

    # Run agio and check output
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        {
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        }
       """)


def test_courses_pk(api_mock):
    """Verify courses subcommand with primary key input.

    $ agio courses 109
    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "109"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        {
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        }
       """)


def test_courses_name(api_mock):
    """Verify courses subcommand with course name input.

    $ agio courses "EECS 485 Spring 2021"
    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "EECS 485 Spring 2021"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        {
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        }
       """)


def test_courses_shortcut(api_mock):
    """Verify courses subcommand with shortcut input.

    $ agio courses eecs485sp21
    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "eecs485sp21"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        {
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        }
       """)