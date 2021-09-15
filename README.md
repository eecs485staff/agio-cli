Autograder.io CLI
=================

[![CI main](https://github.com/eecs485staff/agio-cli/workflows/CI/badge.svg?branch=develop)](https://github.com/eecs485staff/agio-cli/actions?query=branch%3Adevelop)
[![codecov](https://codecov.io/gh/eecs485staff/agio-cli/branch/develop/graph/badge.svg)](https://codecov.io/gh/eecs485staff/agio-cli)
[![PyPI](https://img.shields.io/pypi/v/agiocli.svg)](https://pypi.org/project/agiocli/)

Autograder.io CLI (`agio`) is a command line interface to [autograder.io](https://autograder.io).


## Quick start
First, [obtain a token](#obtaining-a-token) (below).

```console
$ pip install agiocli
$ agio
```

## Obtaining a Token
1. Log in [autograder.io](https://autograder.io/) with your web browser
2. Open browser developer tools
3. Click on a course link
4. In the developer console, click on a request, e.g., `my_roles/` or `projects/`)
5. Under Request Headers, there is an Authorization entry that looks like "Token ". Copy the hex string and save it to the file `.agtoken` in your home
directory.

## Contributing
Contributions from the community are welcome! Check out the [guide for contributing](CONTRIBUTING.md).

## Acknowledgments
Autograder.io CLI is written by Andrew DeOrio <awdeorio@umich.edu>.  Justin Applefield removed bugs and contributed features.

It is based on work by James Perretta ([Autograder.io Contrib](https://github.com/eecs-autograder/autograder-contrib)) and Amir Kamil ([Autograder Tools](https://gitlab.eecs.umich.edu/akamil/autograder-tools/)).
