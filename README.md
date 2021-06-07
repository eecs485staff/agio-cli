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

Test code style
```console
$ pycodestyle agcli setup.py
$ pydocstyle agcli setup.py
$ pylint agcli setup.py
$ check-manifest
```

## Todo
- [x] Pass verbosity to subcommands
- [x] Name that doesn't clash with existing PyPI packages
- [ ] Publish to PyPI
- [x] Automatically call `.json()`
- [ ] User friendly login and logout (token acquisition)
- [ ] Integrate Amir's scripts
- [ ] Integrate EECS 280 scripts
- [ ] Document design philosophy and how to modify
- [ ] Bash and zsh completion
- [x] Guess current semester pk
- [x] Guess current course pk
- [ ] Prompt for {course, project, semester, etc.} pk
- [ ] Open autograder.io web interface similar to `gh pr --web`
- [x] CI runs linters

## Acknowledgments
Autograder.io CLI is written by Andrew DeOrio <awdeorio@umich.edu>

It is based on work by James Perretta ([Autograder.io Contrib](https://github.com/eecs-autograder/autograder-contrib)) and Amir Kamil ([Autograder Tools](https://gitlab.eecs.umich.edu/akamil/autograder-tools/)).
