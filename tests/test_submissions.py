"""System tests for submissions subcommand.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import json
import click
import click.testing
import freezegun
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
    result = runner.invoke(
        main, [
            "submissions",
            "--list",
            "--group", "246965",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    assert "[1125717] 2021-06-09" in result.output
    assert "[1128572] 2021-06-29" in result.output


def test_submissions_pk(api_mock):
    """Verify submissions subcommand with primary key input.

    $ agio submissions 1128572

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, ["submissions", "1128572"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572


def test_submissions_last(api_mock):
    """Verify groups subcommand with 'last' input.

    $ agio submissions \
        --course eecs485sp21 \
        --project p1 \
        --group awdeorio \
        last

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, [
            "submissions",
            "--course", "eecs485sp21",
            "--project", "p1",
            "--group", "awdeorio",
            "last",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572  # awdeorio's latest submission


def test_submissions_best(api_mock):
    """Verify groups subcommand with 'best' input.

    $ agio submissions \
        --course eecs485sp21 \
        --project p1 \
        --group awdeorio \
        best

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, [
            "submissions",
            "--course", "eecs485sp21",
            "--project", "p1",
            "--group", "awdeorio",
            "best",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1125717  # awdeorio's best submission


def test_submissions_empty(api_mock, mocker, constants):
    """Verify submissions subcommand no input.

    $ agio submissions

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109, then project 1005,
    # then submission 1128572.  These are constants in conftest.py. Mock input
    # "awdeorio", which selects a group.
    mocker.patch("pick.pick", side_effect=[
        (constants["COURSE_109"], 1),  # First call to pick() selects course
        (constants["PROJECT_1005"], 0),  # Second call selects project
        (constants["SUBMISSION_1128572"], 0),  # Third call selects submission
    ])
    mocker.patch("builtins.input", return_value="awdeorio")

    # Run agio, mocking the date to be Jun 2021.  We need to mock the date
    # because the prompt filters out past courses.
    # https://github.com/spulec/freezegun
    runner = click.testing.CliRunner()
    with freezegun.freeze_time("2021-06-15"):
        result = runner.invoke(main, ["submissions"], catch_exceptions=False)

    # Check output
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 1128572  # awdeorio's latest submission
