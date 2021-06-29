"""System tests for courses subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import textwrap
import click
import click.testing
from agiocli.__main__ import main


# Unused arguments due to fixtures are endemic to pytest
# pylint: disable=unused-argument


def test_projects_list_course_pk(api_mock):
    """Verify agio projects list option.

    $ agio projects --list --course 109

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "projects",
        "--list",
        "--course", "109",
    ])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        [1005]	Project 1 - Templated Static Site Generator
        [1009]	Project 2 - Server-side Dynamic Pages
        [1008]	Project 3 - Client-side Dynamic Pages
        [1006]	Project 4 - MapReduce
        [1007]	Project 5 - Search Engine
    """)


def test_projects_empty(api_mock, mocker):
    """Verify projects subcommand no input.

    $ agio projects

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109, then project 1005
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
    project_1005 = {
        "pk": 1005,
        "name": "Project 1 - Templated Static Site Generator",
        "last_modified": "2021-05-13T19:46:38.254102Z",
        "course": 109,
        "visible_to_students": True,
        "closing_time": "2021-05-12T04:30:00Z",
        "soft_closing_time": "2021-05-12T03:59:00Z",
        "disallow_student_submissions": False,
        "disallow_group_registration": False,
        "guests_can_submit": True,
        "min_group_size": 1,
        "max_group_size": 1,
        "submission_limit_per_day": 3,
        "allow_submissions_past_limit": False,
        "groups_combine_daily_submissions": False,
        "submission_limit_reset_time": "00:00:00",
        "submission_limit_reset_timezone": "US/Eastern",
        "num_bonus_submissions": 0,
        "total_submission_limit": None,
        "allow_late_days": False,
        "ultimate_submission_policy": "best",
        "hide_ultimate_submission_fdbk": False,
        "instructor_files": [
            {
                "pk": 21908,
                "project": 1005,
                "name": "autograder-6f82202d.tar.gz",
                "last_modified": "2021-04-07T02:16:02.992523Z",
                "size": 11323
            },
            {
                "pk": 21909,
                "project": 1005,
                "name": "install",
                "last_modified": "2021-04-07T02:16:03.147228Z",
                "size": 2230
            }
        ],
        "expected_student_files": [
            {
                "pk": 2545,
                "project": 1005,
                "pattern": "submit.tar.gz",
                "min_num_matches": 1,
                "max_num_matches": 1,
                "last_modified": "2021-04-07T00:31:21.379258Z"
            }
        ],
        "has_handgrading_rubric": False,
        "send_email_on_submission_received": True,
        "send_email_on_non_deferred_tests_finished": True,
        "use_honor_pledge": True,
        "honor_pledge_text": "I have neither given nor received aid on this project, nor have I concealed any violations of the Honor Code."
    }
    mocker.patch("pick.pick", return_value=[
        (course_109, 1),
        (project_1005, 1),
    ])

    # Run agio and check output
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)


def test_projects_pk(api_mock):
    """Verify projects subcommand with primary key input.

    $ agio projects 1008

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "1008"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)


def test_projects_name(api_mock):
    """Verify projects subcommand with project name input.

    $ agio projects -c eecs485sp21 "Project 3 - Client-side Dynamic Pages"

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "projects",
        "-c", "eecs485sp21",
        "Project 3 - Client-side Dynamic Pages",
    ])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)


def test_projects_shortcut(api_mock):
    """Verify projects subcommand with shortcut input.

    $ agio projects -c eecs485sp21 p3

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "projects",
        "-c", "eecs485sp21",
        "p3",
    ])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)


def test_projects_no_course(api_mock):
    """Verify projects subcommand with no --course specified.

    $ agio projects p3

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # FIXME mock course selection picker
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "p3"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)
