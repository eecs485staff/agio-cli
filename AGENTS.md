# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## Overview

`agio` is a command line interface to [autograder.io](https://autograder.io), distributed on PyPI as the `agiocli` package.  It wraps the autograder.io REST API and adds "smart" selection: instructors can refer to courses, projects, groups, and submissions by human shorthand (`eecs485sp21`, `p1`, a uniqname) instead of database primary keys.

## Commands

Install for development:
```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --editable .[dev,test]
```

Run tests, coverage, and a single test:
```console
$ pytest
$ pytest -vv --log-cli-level=DEBUG          # verbose
$ pytest --cov ./agiocli --cov-report term-missing
$ pytest tests/test_courses.py::test_courses_pk
```

Lint (all four must pass; this is what CI runs):
```console
$ pycodestyle agiocli tests setup.py
$ pydocstyle agiocli tests setup.py
$ pylint agiocli tests setup.py
$ check-manifest
```

Run the full lint + test suite in a clean throwaway virtualenv (mirrors CI exactly):
```console
$ tox -e py3
```

Note: pydocstyle cannot glob `tests/`, so tox invokes it as `sh -c "pydocstyle agiocli tests/* setup.py"`.  When running pydocstyle manually against tests, match that pattern.

## Architecture

Three modules under `agiocli/`, layered:

- `__main__.py` - Click CLI.  A top-level `main` group with five subcommands: `login`, `courses`, `projects`, `groups`, `submissions`.  Each subcommand is thin: it builds an `APIClient`, then delegates all logic to `utils`.  The `--debug` flag is stored on the Click context object and threaded into the client.

- `api_client.py` - `APIClient`, a thin authenticated wrapper over `requests` (get/post/put/patch/delete plus `get_paginated`).  `APIClient.make_default()` is the intended constructor.  It finds the API token by walking up from the current directory to `$HOME` looking for `.agtoken` (see `get_api_token`/`walk_up_to_home_dir`).  `do_request` injects the `Authorization: Token ...` header, checks status, and decodes JSON or octet-stream (file downloads) responses.  On any HTTP error it calls `sys.exit` with a message rather than raising.

- `utils.py` - All the real logic.  Two categories of function:
  - **Parsing**: `parse_course_string` (e.g. `eecs485sp21` -> `(2021, 'Spring', 'EECS 485')`) and `parse_project_string` (e.g. `p4mapreduce` -> `('Project', 4, 'mapreduce')`).  Both use verbose regexes with abbreviation lookup tables.  Defaulting to the current semester and to the `EECS` department happens here.
  - **Smart selection**: `get_<thing>_smart()` for course/project/group/submission.  These share a consistent resolution strategy: if the arg is numeric, treat it as a primary key and fetch directly; otherwise resolve the parent entity (a project needs a course, a group needs a project, etc.) by recursively calling the parent's `get_*_smart`, fetch the list, then either match the user's string or, if no arg was given, prompt interactively.  Matching that is ambiguous or empty exits with an error listing the candidates.

The selection chain is the key design idea: `submission -> group -> project -> course`.  Each level can be supplied explicitly via a flag (`-c`, `-p`, `-g`) or left to interactive selection.

Interactive prompts use `pick` (arrow-key menus) for courses/projects/submissions and `readline` tab-completion for group member uniqnames.

## Testing

Tests are system tests driven through Click's `CliRunner` (`runner.invoke(main, [...])`), asserting on `exit_code` and `output`.  Key fixtures in `tests/conftest.py`:

- `api_mock` - mocks all autograder.io REST endpoints with `requests-mock`, returning canned JSON.  Most tests just request this fixture.
- `mocker.patch("pick.pick", ...)` - simulates a user's interactive menu choice.
- `freezegun.freeze_time(...)` - pins "today" so current-semester defaulting is deterministic.

`tests/conftest.py` imports `utils` directly, so `tox` sets `PYTHONPATH={toxinidir}`.  Canned constants and the config fixture live in `conftest.py` and `tests/testdata/`.

## Conventions

- Errors surfaced to the user are reported via `sys.exit("Error: ...")`, not exceptions, except `TokenFileNotFound` and `UnsupportedAssignmentError` which are caught by callers.
- Click docstrings use `\b` to prevent paragraph rewrapping; lines with `\b` carry a `# noqa: D301`.
- Subcommands with many params carry `# pylint: disable=too-many-arguments` because each CLI option needs a function parameter.
- The version string lives in `setup.py` (`version=`); bumping it is a manual step in the release procedure.

## Release

`develop` is the default working branch; releases are merged to `main` and tagged.  Full procedure (version bump, tox, tag, Test PyPI, PyPI, GitHub release) is in [CONTRIBUTING.md](CONTRIBUTING.md).
