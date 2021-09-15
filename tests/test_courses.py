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


def test_courses_list(api_mock):
    """Verify agio courses list option.

    $ agio courses --list

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "--list"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert result.output == textwrap.dedent("""\
        [129] EECS 485 Fall 2021
        [109] EECS 485 Spring 2021
        [111] EECS 280 Spring 2021
        [1] EECS 280 Fall 2016
    """)


def test_courses_empty(api_mock, mocker):
    """Verify courses subcommand no input.

    $ agio courses

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

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

    # Run agio, mocking the date to be Jun 2021.  We need to mock the date
    # because the prompt filters out past courses.
    # https://github.com/spulec/freezegun
    runner = click.testing.CliRunner()
    with freezegun.freeze_time("2021-06-15"):
        result = runner.invoke(main, ["courses"], catch_exceptions=False)

    # Check output
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 109


def test_courses_pk(api_mock):
    """Verify courses subcommand with primary key input.

    $ agio courses 109

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "109"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 109


def test_courses_name(api_mock):
    """Verify courses subcommand with course name input.

    $ agio courses "EECS 485 Spring 2021"

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, ["courses", "EECS 485 Spring 2021"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 109


def test_courses_shortcut(api_mock):
    """Verify courses subcommand with shortcut input.

    $ agio courses eecs485sp21

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, ["courses", "eecs485sp21"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 109
