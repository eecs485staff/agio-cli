"""
System tests for the command line interface.

These tests use the Click testing interface.
https://click.palletsprojects.com/en/8.0.x/testing/
"""
import click
import click.testing
from agiocli.__main__ import main


def test_example():
    """Dummy example test."""
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(main, ["--version"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert "version" in result.output
