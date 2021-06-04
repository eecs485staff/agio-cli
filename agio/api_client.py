"""
Autograder REST API client, a wrapper around the requests library.

Based on HTTPClient by James Perretta
https://github.com/eecs-autograder/autograder-contrib/
"""
import copy
import os
import json
from typing import Iterator
from urllib.parse import urljoin
import requests


class APIClient:
    """Send authenticated requests to the autograder.io REST API.

    APIClient is a wrapper around the requests library that adds an
    authentication token to the headers.  It supports all the arguments
    accepted by the corresponding requests library methods.
    https://requests.readthedocs.io/

    Avoid constructing HTTPClient directly.  Instead, use
    APIClient.make_default().
    """

    @staticmethod
    def make_default(
            token_filename='.agtoken',
            base_url='https://autograder.io/',
            debug=False
    ):
        """Create an APIClient instance with API token found in token_filename.

        Token file discovery works as follows:
        - If token_filename is just a filename (no path information),
        the current directory and every upward directory until the home
        directory will be searched for a file with that name.
        - If token_filename is an absolute path or a relative path that
        contains at least one directory, that file will be opened and
        the token read to it.

        base_url will be prepended to all URLs passed to the client's
        request methods and defaults to https://autograder.io/.
        """
        return APIClient(get_api_token(token_filename), base_url, debug)

    def __init__(self, api_token, base_url, debug=False):
        """Create an APIClient instance using a raw api_token.

        Most users should use HTTPClient.make_default() instead.
        """
        self.api_token = api_token
        self.base_url = base_url
        self.debug = debug

    def get(self, path, *args, **kwargs):
        """Call requests.get with authentication headers and base URL."""
        return self.do_request(requests.get, path, *args, **kwargs)

    def get_paginated(self, path, *args, **kwargs):
        """Iterate over paginated list route, yielding one page at a time."""
        page_url = path
        while page_url:
            response = self.get(page_url, *args, **kwargs)
            response.raise_for_status()
            assert "results" in response.json()
            assert "next" in response.json()
            for item in response.json()["results"]:
                yield item
            page_url = response.json()['next']

    def post(self, path, *args, **kwargs):
        """Call requests.post with authentication headers and base URL."""
        return self.do_request(requests.post, path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        """Call requests.put with authentication headers and base URL."""
        return self.do_request(requests.put, path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        """Call requests.patch with authentication headers and base URL."""
        return self.do_request(requests.patch, path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        """Call requests.delete with authentication headers and base URL."""
        return self.do_request(requests.delete, path, *args, **kwargs)

    def do_request(self, method_func, path, *args, **kwargs):
        """Add authentication headers and base URL, then call method_func.

        - Append path to autograder REST API base URL
        - Add token authentication headers
        - Call method_func
        - Check HTTP status code and raise HTTPError if necessary
        - Parse JSON if present
        """
        url = urljoin(self.base_url, path)
        headers = copy.deepcopy(kwargs.pop('headers', {}))
        headers['Authorization'] = f'Token {self.api_token}'
        if self.debug:
            method = method_func.__name__.upper()
            print(f"{method} {url}")
        response = method_func(url, *args, headers=headers, **kwargs)
        if self.debug:
            print_response(response)
        response.raise_for_status()
        breakpoint()
        # FIXME check for exception, check if actually JSON
        return response.json()


def get_api_token(token_filename: str) -> str:
    """Search for autograder.io token.

    Token file discovery works as follows:
    - If token_filename is just a filename (no path information), the current
      directory and every upward directory until the home directory will be
      searched for a file with that name.
    - If token_filename is an absolute path or a relative path that contains
      at least one directory, that file will be opened and the token read.
    """
    token_not_found_msg = f'Requested token file: {token_filename} not found'
    if os.path.dirname(token_filename) and not os.path.isfile(token_filename):
        raise TokenFileNotFound(token_not_found_msg)

    # Make sure that we're starting in a subdir of the home directory
    if os.path.expanduser('~') not in os.path.abspath(os.curdir):
        raise TokenFileNotFound(token_not_found_msg)

    for dirname in walk_up_to_home_dir():
        filename = os.path.join(dirname, token_filename)
        if os.path.isfile(filename):
            with open(filename) as tokenfile:
                return tokenfile.read().strip()

    raise TokenFileNotFound(token_not_found_msg)


def walk_up_to_home_dir() -> Iterator[str]:
    """Iterate up the directory structure from pwd to home directory."""
    current_dir = os.path.abspath(os.curdir)
    home_dir = os.path.expanduser('~')

    while current_dir != home_dir:
        yield current_dir
        current_dir = os.path.dirname(current_dir)

    yield home_dir


def print_response(response):
    """Print a response object."""
    try:
        parsed = response.json()
    except json.JSONDecodeError:
        print(response.text)
    else:
        formatted = json.dumps(parsed, indent=4)
        print(formatted)


class TokenFileNotFound(Exception):
    """Exception type indicating failure to locate user token file."""
