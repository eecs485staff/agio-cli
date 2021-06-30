"""System tests for submissions subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import json
import click
import click.testing
from agiocli.__main__ import main


# Unused arguments due to fixtures are endemic to pytest
# pylint: disable=unused-argument


def test_submissions_list(api_mock):
    """Verify agio submissions list option when group is specified.

    $ agio submissions --list --group 246965

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "submissions",
        "--list",
        "--group", "246965",
    ])
    assert result.exit_code == 0
    assert "[1125717] 2021-06-09" in result.output
    assert "[1128572] 2021-06-29" in result.output


def test_submissions_pk(api_mock):
    """Verify submissions subcommand with primary key input.

    $ agio submissions 1128572

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["submissions", "1128572"])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572


def test_submissions_uniqname(api_mock):
    """Verify groups subcommand with group member uniqname input.

    $ agio submissions \
        --course eecs485sp21 \
        --project p1 \
        --group awdeorio

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, [
        "submissions",
        "--course", "eecs485sp21",
        "--project", "p1",
        "--group", "awdeorio",
    ])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572  # awdeorio's latest submission


def test_submissions_empty(api_mock, mocker, constants):
    """Verify submissions subcommand no input.

    $ agio submissions

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109, then project 1005,
    # then group 246965.  These are constants in conftest.py
    mocker.patch("pick.pick", side_effect=[
        (constants["COURSE_109"], 1),  # First call to pick() selects course
        (constants["PROJECT_1005"], 0),  # Second call selects project
        (constants["GROUP_246965"], 0),  # Third call selects group
    ])

    # Run agio and check output
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["submissions"])
    assert result.exit_code == 0
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572  # awdeorio's latest submission