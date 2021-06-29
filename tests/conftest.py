"""Shared test fixtures."""
import json
import textwrap
import pytest


@pytest.fixture(name="api_mock")
def api_requests_mock(requests_mock):
    """Mock Autograder API with hardcoded responses."""
    # User
    requests_mock.get(
        "https://autograder.io/api/users/current/",
        text=textwrap.dedent("""\
        {
            "pk": 5,
            "username": "awdeorio@umich.edu",
            "first_name": "Andrew",
            "last_name": "DeOrio",
            "email": "",
            "is_superuser": false
        }
        """)
    )
    # Course list
    requests_mock.get(
        "https://autograder.io/api/users/5/courses_is_admin_for/",
        text=json.dumps([
            {
                "pk": 111,
                "name": "EECS 280",
                "semester": "Spring",
                "year": 2021,
                "subtitle": "",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-05-03T01:12:28.049482Z"
            },
            {
                "pk": 109,
                "name": "EECS 485",
                "semester": "Spring",
                "year": 2021,
                "subtitle": "Web Systems",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-04-07T02:19:22.818992Z"
            },
            {
                "pk": 129,
                "name": "EECS 485",
                "semester": "Fall",
                "year": 2021,
                "subtitle": "Web Systems",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2021-06-23T13:54:07.942973Z"
            }
        ])
    )
    # Course detail
    requests_mock.get(
        "https://autograder.io/api/courses/109/",
        text=json.dumps({
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        })
    )
