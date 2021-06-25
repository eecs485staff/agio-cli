"""System tests for courses subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import textwrap
import click
import click.testing
import pytest
from agiocli.__main__ import main


@pytest.fixture
def api_mock(requests_mock):
    """Mock Autograder API with hardcoded responses."""
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
    requests_mock.get(
        "https://autograder.io/api/users/5/courses_is_admin_for/",
        text=textwrap.dedent("""\
        [
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
        ]
        """)
        )


def test_courses_list(api_mock):
    """Verify agio courses --list."""
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(main, ["courses", "--list"])
    assert result.exit_code == 0
    assert result.output == '[129]\tEECS 485 Fall 2021\n[109]\tEECS 485 Spring 2021\n[111]\tEECS 280 Spring 2021\n'
    assert result.output == textwrap.dedent("""\
        [129]\tEECS 485 Fall 2021
        [109]\tEECS 485 Spring 2021
        [111]\tEECS 280 Spring 2021
    """)
