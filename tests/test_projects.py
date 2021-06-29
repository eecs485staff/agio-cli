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
    assert False, "IMPLEMENT ME"


def test_projects_list(api_mock):
    """Verify agio projects list option.

    $ agio projects --list
    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "--list"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        [129]\tEECS 485 Fall 2021
        [109]\tEECS 485 Spring 2021
        [111]\tEECS 280 Spring 2021
    """)


def test_projects_empty(api_mock, mocker):
    """Verify projects subcommand no input.

    $ agio projects
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
    mocker.patch("pick.pick", return_value=(project_109, 1))

    # FIXME: Mock user-selection menu, users selects project pk 1008

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
    """
    # FIXME mock course selection picker
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "p3"])
    assert result.exit_code == 0
    assert result.output == textwrap.dedent("""\
        FIXME
    """)
