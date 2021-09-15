Contributing to agio-cli
========================

## Install development environment
Set up a development virtual environment.
```console
$ python3 -m venv .venv
$ source env/bin/activate
$ pip install --editable .[dev,test]
```

A `agio` entry point script is installed in your virtual environment.
```console
$ which agio
/Users/awdeorio/src/mailmerge/.venv/bin/agio
```

## Testing and code quality
Run unit tests
```console
$ pytest
$ pytest -vv --log-cli-level=DEBUG  # More output
```

Measure unit test case coverage
```console
$ pytest --cov ./agiocli --cov-report term-missing
```

Test code style
```console
$ pycodestyle agiocli tests setup.py
$ pydocstyle agiocli tests setup.py
$ pylint agiocli tests setup.py
$ check-manifest
```

Run linters and tests in a clean environment.  This will automatically create a temporary virtual environment.
```console
$ tox -e py3
```

## Release procedure
Update your local `develop` branch.  Make sure it's clean.
```console
$ git fetch
$ git checkout develop
$ git rebase
$ git status
```

Test
```console
$ tox -e py3
```

Update version
```console
$ $EDITOR setup.py
$ git commit -m "version bump" setup.py
$ git push origin develop
```

Update main branch
```console
$ git fetch
$ git checkout main
$ git rebase
$ git merge --no-ff origin/develop
```

Build distribution binary and source tarball locally
```console
$ rm -rf dist
$ python3 setup.py sdist bdist_wheel
$ ls dist
agiocli-0.1.0-py3-none-any.whl  agiocli-0.1.0.tar.gz
```

Tag a release
```console
$ git tag -a X.Y.Z
$ grep version= setup.py
    version="X.Y.Z",
$ git describe
X.Y.Z
$ git push --tags origin main
```

Deploy to Test PyPI, then browse to https://test.pypi.org/project/agiocli/
```console
$ twine upload --sign --repository-url https://test.pypi.org/legacy/ dist/*
```

Test install.  It will install, but not run because we didn't install deps.
```console
$ python3 -m venv testenv
$ source testenv/bin/activate
$ pip install --index-url https://test.pypi.org/simple/ --no-deps agiocli
$ agio --version  # Expect module not found error
$ deactivate
```

Deploy to PyPI, then browse to https://pypi.org/project/agiocli/
```console
$ twine upload --sign dist/*
```

Test install from new PyPI deploy
```console
$ pip3 install --upgrade agiocli
$ agio --version
agio, version X.Y.Z
```
