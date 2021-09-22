"""System tests for groups subcommand.

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


def test_groups_list(api_mock):
    """Verify agio groups list option when project is specified.

    $ agio groups --list --project 1005

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, [
            "groups",
            "--list",
            "--project", "1005",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    assert "[243636] achitta" in result.output
    assert "[246965] awdeorio" in result.output


def test_groups_pk(api_mock):
    """Verify groups subcommand with primary key input.

    $ agio groups 246965

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["groups", "246965"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 246965
    assert output_obj["members"] == [
        {
            'email': '',
            'first_name': 'Andrew',
            'is_superuser': False,
            'last_name': 'DeOrio',
            'pk': 5,
            'username': 'awdeorio@umich.edu',
        },
    ]


def test_groups_uniqname(api_mock):
    """Verify groups subcommand with group member uniqname input.

    $ agio groups \
        --course eecs485sp21 \
        --project p1 \
        awdeorio

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main, [
            "groups",
            "--course", "eecs485sp21",
            "--project", "p1",
            "awdeorio",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 246965  # awdeorio's group


def test_groups_empty(api_mock, mocker, constants):
    """Verify groups subcommand no input.

    $ agio groups

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    # Mock user-selection menu, users selects course 109, then project 1005.
    # These are constants in conftest.py.  Mock input "awdeorio", which selects
    # a group.
    mocker.patch("pick.pick", side_effect=[
        (constants["COURSE_109"], 1),  # First call to pick() selects course
        (constants["PROJECT_1005"], 0),  # Second call selects project
    ])
    mocker.patch("builtins.input", return_value="awdeorio")

    # Run agio, mocking the date to be Jun 2021.  We need to mock the date
    # because the prompt filters out past courses.
    # https://github.com/spulec/freezegun
    runner = click.testing.CliRunner()
    with freezegun.freeze_time("2021-06-15"):
        result = runner.invoke(main, ["groups"], catch_exceptions=False)

    # Check output
    assert result.exit_code == 0, result.output
    output_obj = json.loads(result.output)
    assert output_obj["pk"] == 246965  # awdeorio's group
