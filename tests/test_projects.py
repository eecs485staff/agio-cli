"""System tests for courses subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import json
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


def test_projects_pk(api_mock):
    """Verify projects subcommand with primary key input.

    $ agio projects 1005

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "1005"])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005
    assert output_obj["name"] == "Project 1 - Templated Static Site Generator"


def test_projects_name(api_mock):
    """Verify projects subcommand with project name input.

    $ agio projects -c eecs485sp21 \
        "Project 1 - Templated Static Site Generator"

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "projects",
        "-c", "eecs485sp21",
        "Project 1 - Templated Static Site Generator",
    ])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005
    assert output_obj["name"] == "Project 1 - Templated Static Site Generator"


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
        "p1",
    ])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005


def test_projects_no_course(api_mock, mocker):
    """Verify projects subcommand with no --course specified.

    $ agio projects p3

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109
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

    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "p1"])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005


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
    }
    mocker.patch("pick.pick", side_effect=[
        (course_109, 1),  # First call to pick() selects course
        (project_1005, 0),  # Second  call to pick() selects project
    ])

    # Run agio and check output
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects"])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005
