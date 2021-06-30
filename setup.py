"""Autograder.io CLI build and install configuration."""
import os
import io
import setuptools


# Read the contents of README file
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(PROJECT_DIR, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name="agiocli",
    description="A command line interface to autograder.io",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version="0.1.0",
    author="Andrew DeOrio",
    author_email="awdeorio@umich.edu",
    url="https://github.com/eecs485staff/agio-cli/",
    license="MIT",
    packages=["agiocli"],
    keywords=[
        "autograder", "autograder.io", "auto grader",
        "agcli", "agio", "ag-cli", "agio-cli",
    ],
    install_requires=[
        "click",
        "pick",
        "requests",
    ],
    extras_require={
        "dev": [
            "pdbpp",
            "twine",
            "check-manifest",
            "pycodestyle",
            "pydocstyle",
            "pylint",
            "pytest",
            "pytest-mock",
            "python-dateutil",
            "requests-mock",
        ],
    },
    python_requires='>=3.6',

    # Python command line utilities will be installed in a PATH-accessible bin/
    entry_points={
        "console_scripts": [
            "agio = agiocli.__main__:main",
        ]
    },
)
