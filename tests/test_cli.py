"""
System tests for the command line interface.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import textwrap
import click
import click.testing
from agiocli.__main__ import main


# Unused arguments due to fixtures are endemic to pytest
# pylint: disable=unused-argument


def test_example():
    """Dummy example test."""
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0, result.output
    assert "version" in result.output


def test_courses_list(api_mock):
    """Verify agio courses list option.

    $ agio courses --list

    api_mock is a shared test fixture that mocks responses to REST API
    requests.  It is implemented in conftest.py.

    """
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["courses", "--list"])
    for k,v in result.__dict__.items():
        print(f"DEBUG: {k}:{v}")
    assert result.exit_code == 0, result.output
    assert result.output == textwrap.dedent("""\
        [129]\tEECS 485 Fall 2021
        [109]\tEECS 485 Spring 2021
        [111]\tEECS 280 Spring 2021
        [1]\tEECS 280 Fall 2016
    """)
