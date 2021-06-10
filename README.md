Autograder.io CLI
=================

Autograder.io CLI (`agio`) is a command line interface to [autograder.io](https://autograder.io).


## Quick start
```console
FIXME
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
$ pip install -e .[dev]
```

Run tests
```console
$ pytest tests
```

Test code style
```console
$ pycodestyle agcli tests setup.py
$ pydocstyle agcli tests setup.py
$ pylint agcli tests setup.py
$ check-manifest
```

## Acknowledgments
Autograder.io CLI is written by Andrew DeOrio <awdeorio@umich.edu>

It is based on work by James Perretta ([Autograder.io Contrib](https://github.com/eecs-autograder/autograder-contrib)) and Amir Kamil ([Autograder Tools](https://gitlab.eecs.umich.edu/akamil/autograder-tools/)).
