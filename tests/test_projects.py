"""System tests for courses subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import json
import textwrap
import click
import click.testing
import freezegun
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
    result = runner.invoke(
        main, ["projects", "--list", "--course", "109"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    assert result.output == textwrap.dedent("""\
        [1005] Project 1 - Templated Static Site Generator
        [1009] Project 2 - Server-side Dynamic Pages
        [1008] Project 3 - Client-side Dynamic Pages
        [1006] Project 4 - MapReduce
        [1007] Project 5 - Search Engine
    """)


def test_projects_pk(api_mock):
    """Verify projects subcommand with primary key input.

    $ agio projects 1005

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["projects", "1005"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
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
    result = runner.invoke(
        main, [
            "projects",
            "--course", "eecs485sp21",
            "Project 1 - Templated Static Site Generator",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
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
    result = runner.invoke(
        main, [
            "projects",
            "-c", "eecs485sp21",
            "p1",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005


def test_projects_no_course(api_mock, mocker, constants):
    """Verify projects subcommand with no --course specified.

    $ agio projects p3

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109.  This constant is
    # defined in conftest.py
    mocker.patch("pick.pick", return_value=(constants["COURSE_109"], 1))

    # Run agio, mocking the date to be Jun 2021.  We need to mock the date
    # because the prompt filters out past courses.
    # https://github.com/spulec/freezegun
    runner = click.testing.CliRunner()
    with freezegun.freeze_time("2021-06-15"):
        result = runner.invoke(
            main, ["projects", "p1"],
            catch_exceptions=False,
        )

    # Check output
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005


def test_projects_empty(api_mock, mocker, constants):
    """Verify projects subcommand no input.

    $ agio projects

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109, then project 1005.
    # These constants are defined in conftest.py
    mocker.patch("pick.pick", side_effect=[
        (constants["COURSE_109"], 1),  # First call to pick() selects course
        (constants["PROJECT_1005"], 0),  # Second  call selects project
    ])

    # Run agio, mocking the date to be Jun 2021.  We need to mock the date
    # because the prompt filters out past courses.
    # https://github.com/spulec/freezegun
    runner = click.testing.CliRunner()
    with freezegun.freeze_time("2021-06-15"):
        result = runner.invoke(main, ["projects"], catch_exceptions=False)

    # Check output
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1005
