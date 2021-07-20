Autograder.io CLI
=================

Autograder.io CLI (`agio`) is a command line interface to [autograder.io](https://autograder.io).


## Quick start
First, [obtain a token](#obtaining-a-token) (below).

```console
$ pip install agiocli
$ agiocli
```

## Obtaining a Token
1. Log in [autograder.io](https://autograder.io/) with your web browser
2. Open browser developer tools
3. Click on a course link
4. In the developer console, click on a request, e.g., `my_roles/` or `projects/`)
5. Under Request Headers, there is an Authorization entry that looks like "Token ". Copy the hex string and save it to the file `.agtoken` in your home
directory.

## Contributing
Install
```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .[dev,test]
```

Run tests
```console
$ pytest
$ pytest -vv --log-cli-level=DEBUG
```

Test code style
```console
$ pycodestyle agiocli tests setup.py
$ pydocstyle agiocli tests setup.py
$ pylint agiocli tests setup.py
$ check-manifest
```

Regression, including tests and style checks
```console
$ tox
```

## Acknowledgments
Autograder.io CLI is written by Andrew DeOrio <awdeorio@umich.edu>.  Justin Applefield removed bugs and contributed features.

It is based on work by James Perretta ([Autograder.io Contrib](https://github.com/eecs-autograder/autograder-contrib)) and Amir Kamil ([Autograder Tools](https://gitlab.eecs.umich.edu/akamil/autograder-tools/)).
