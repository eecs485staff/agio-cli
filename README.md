Autograder.io CLI
=================

Autograder.io CLI (`agio`) is a command line interface to [autograder.io](https://autograder.io).

Andrew DeOrio <awdeorio@umich.edu>


## Quick start
```console
FIXME
```

FIXME how to get a token


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
- [ ] Verbose levels
- [ ] Centralized error handling
- [ ] Centralize token acquisition and error handling
- [ ] Pass verbosity to subcommands
- [x] Name that doesn't clash with existing PyPI packages
- [ ] Publish to PyPI
- [ ] Design for file download
- [ ] Automatically call `.json()`?
- [ ] User friendly login and logout (token acquisition)
- [ ] Integrate Amir's scripts
- [ ] Integrate EECS 280 scripts
- [ ] Document design philosophy and how to modify
- [ ] Bash and zsh completion
- [ ] Guess current semester pk
- [ ] Guess current course pk
- [ ] Prompt for {course, project, semester, etc.} pk
- [ ] Open autograder.io web interface similar to `gh pr --web`
