"""Shared test fixtures."""
import json
import pytest


@pytest.fixture(name="api_mock")
def api_requests_mock(requests_mock):
    """Mock Autograder API with hardcoded responses."""
    # User
    requests_mock.get(
        "https://autograder.io/api/users/current/",
        text=json.dumps({
            "pk": 5,
            "username": "awdeorio@umich.edu",
            "first_name": "Andrew",
            "last_name": "DeOrio",
            "email": "",
            "is_superuser": False
        })
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

    # Project list
    requests_mock.get(
        "https://autograder.io/api/courses/109/projects/",
        text=json.dumps([
            {
                "pk": 1007,
                "name": "Project 5 - Search Engine",
                "last_modified": "2021-06-21T16:42:49.476960Z",
                "course": 109,
                "visible_to_students": True,
                "closing_time": "2021-06-21T04:30:00Z",
                "soft_closing_time": "2021-06-21T03:59:00Z",
                "disallow_student_submissions": False,
                "disallow_group_registration": False,
                "guests_can_submit": False,
                "min_group_size": 1,
                "max_group_size": 3,
                "submission_limit_per_day": 3,
                "allow_submissions_past_limit": False,
                "groups_combine_daily_submissions": False,
                "submission_limit_reset_time": "00:00:00",
                "submission_limit_reset_timezone": "US/Eastern",
                "num_bonus_submissions": 0,
                "total_submission_limit": None,
                "allow_late_days": False,
                "ultimate_submission_policy": "best",
                "hide_ultimate_submission_fdbk": False,
                "instructor_files": [
                    {
                        "pk": 24749,
                        "project": 1007,
                        "name": "autograder-4d215e29.tar.xz",
                        "last_modified": "2021-06-14T03:39:17.838619Z",
                        "size": 4306452
                    },
                    {
                        "pk": 24750,
                        "project": 1007,
                        "name": "install",
                        "last_modified": "2021-06-14T03:39:18.125266Z",
                        "size": 2906
                    }
                ],
                "expected_student_files": [
                    {
                        "pk": 2547,
                        "project": 1007,
                        "pattern": "submit.tar.xz",
                        "min_num_matches": 1,
                        "max_num_matches": 1,
                        "last_modified": "2021-04-07T00:31:28.029083Z"
                    }
                ],
                "has_handgrading_rubric": False,
                "send_email_on_submission_received": True,
                "send_email_on_non_deferred_tests_finished": True,
                "use_honor_pledge": True,
                "honor_pledge_text": (
                    "I have neither given nor received aid on this project, "
                    "nor have I concealed any violations of the Honor Code."
                )
            },
            {
                "pk": 1008,
                "name": "Project 3 - Client-side Dynamic Pages",
                "last_modified": "2021-05-27T22:01:15.359868Z",
                "course": 109,
                "visible_to_students": True,
                "closing_time": "2021-05-26T04:30:00Z",
                "soft_closing_time": "2021-05-26T03:59:00Z",
                "disallow_student_submissions": False,
                "disallow_group_registration": False,
                "guests_can_submit": False,
                "min_group_size": 1,
                "max_group_size": 3,
                "submission_limit_per_day": 3,
                "allow_submissions_past_limit": False,
                "groups_combine_daily_submissions": False,
                "submission_limit_reset_time": "00:00:00",
                "submission_limit_reset_timezone": "US/Eastern",
                "num_bonus_submissions": 0,
                "total_submission_limit": None,
                "allow_late_days": False,
                "ultimate_submission_policy": "best",
                "hide_ultimate_submission_fdbk": False,
                "instructor_files": [
                    {
                        "pk": 22508,
                        "project": 1008,
                        "name": "autograder-bcc78f56-dirty.tar.gz",
                        "last_modified": "2021-05-18T22:00:36.641145Z",
                        "size": 168836
                    },
                    {
                        "pk": 21949,
                        "project": 1008,
                        "name": "install",
                        "last_modified": "2021-05-18T22:00:36.805560Z",
                        "size": 3057
                    }
                ],
                "expected_student_files": [
                    {
                        "pk": 2548,
                        "project": 1008,
                        "pattern": "submit.tar.gz",
                        "min_num_matches": 1,
                        "max_num_matches": 1,
                        "last_modified": "2021-04-07T00:31:30.640369Z"
                    }
                ],
                "has_handgrading_rubric": False,
                "send_email_on_submission_received": True,
                "send_email_on_non_deferred_tests_finished": True,
                "use_honor_pledge": True,
                "honor_pledge_text": (
                    "I have neither given nor received aid on this project, "
                    "nor have I concealed any violations of the Honor Code."
                )
            },
            PROJECT_1005,
            {
                "pk": 1009,
                "name": "Project 2 - Server-side Dynamic Pages",
                "last_modified": "2021-05-19T13:03:53.221672Z",
                "course": 109,
                "visible_to_students": True,
                "closing_time": "2021-05-19T04:30:00Z",
                "soft_closing_time": "2021-05-19T03:59:00Z",
                "disallow_student_submissions": False,
                "disallow_group_registration": False,
                "guests_can_submit": False,
                "min_group_size": 1,
                "max_group_size": 3,
                "submission_limit_per_day": 3,
                "allow_submissions_past_limit": False,
                "groups_combine_daily_submissions": False,
                "submission_limit_reset_time": "00:00:00",
                "submission_limit_reset_timezone": "US/Eastern",
                "num_bonus_submissions": 0,
                "total_submission_limit": None,
                "allow_late_days": False,
                "ultimate_submission_policy": "best",
                "hide_ultimate_submission_fdbk": False,
                "instructor_files": [
                    {
                        "pk": 22506,
                        "project": 1009,
                        "name": "autograder-788e5076.tar.gz",
                        "last_modified": "2021-05-11T19:21:55.373807Z",
                        "size": 282326
                    },
                    {
                        "pk": 22507,
                        "project": 1009,
                        "name": "install",
                        "last_modified": "2021-05-11T19:21:55.596257Z",
                        "size": 2095
                    }
                ],
                "expected_student_files": [
                    {
                        "pk": 2549,
                        "project": 1009,
                        "pattern": "submit.tar.gz",
                        "min_num_matches": 1,
                        "max_num_matches": 1,
                        "last_modified": "2021-04-07T00:31:33.584510Z"
                    }
                ],
                "has_handgrading_rubric": False,
                "send_email_on_submission_received": True,
                "send_email_on_non_deferred_tests_finished": True,
                "use_honor_pledge": True,
                "honor_pledge_text": (
                    "I have neither given nor received aid on this project, "
                    "nor have I concealed any violations of the Honor Code."
                )
            },
            {
                "pk": 1006,
                "name": "Project 4 - MapReduce",
                "last_modified": "2021-06-15T03:59:11.942724Z",
                "course": 109,
                "visible_to_students": True,
                "closing_time": "2021-06-14T04:30:00Z",
                "soft_closing_time": "2021-06-14T03:59:00Z",
                "disallow_student_submissions": False,
                "disallow_group_registration": False,
                "guests_can_submit": False,
                "min_group_size": 1,
                "max_group_size": 3,
                "submission_limit_per_day": 3,
                "allow_submissions_past_limit": False,
                "groups_combine_daily_submissions": False,
                "submission_limit_reset_time": "00:00:00",
                "submission_limit_reset_timezone": "US/Eastern",
                "num_bonus_submissions": 0,
                "total_submission_limit": None,
                "allow_late_days": False,
                "ultimate_submission_policy": "best",
                "hide_ultimate_submission_fdbk": False,
                "instructor_files": [
                    {
                        "pk": 21900,
                        "project": 1006,
                        "name": "autograder-8b2ec48d.tar.gz",
                        "last_modified": "2021-04-07T00:31:25.318107Z",
                        "size": 3077619
                    },
                    {
                        "pk": 21901,
                        "project": 1006,
                        "name": "install",
                        "last_modified": "2021-04-07T00:31:25.441090Z",
                        "size": 2098
                    }
                ],
                "expected_student_files": [
                    {
                        "pk": 2546,
                        "project": 1006,
                        "pattern": "submit.tar.gz",
                        "min_num_matches": 1,
                        "max_num_matches": 1,
                        "last_modified": "2021-04-07T00:31:25.503082Z"
                    }
                ],
                "has_handgrading_rubric": False,
                "send_email_on_submission_received": True,
                "send_email_on_non_deferred_tests_finished": True,
                "use_honor_pledge": True,
                "honor_pledge_text": (
                    "I have neither given nor received aid on this project, "
                    "nor have I concealed any violations of the Honor Code."
                )
            }
        ])
    )

    # Project detail
    requests_mock.get(
        "https://autograder.io/api/projects/1005/",
        text=json.dumps(PROJECT_1005),
    )


PROJECT_1005 = {
    "pk": 1005,
    "name": "Project 1 - Templated Static Site Generator",
    "last_modified": "2021-05-13T19:46:38.254102Z",
    "course": 109,
    "visible_to_students": True,
    "closing_time": "2021-05-12T04:30:00Z",
    "soft_closing_time": "2021-05-12T03:59:00Z",
    "disallow_student_submissions": False,
    "disallow_group_registration": False,
    "guests_can_submit": True,
    "min_group_size": 1,
    "max_group_size": 1,
    "submission_limit_per_day": 3,
    "allow_submissions_past_limit": False,
    "groups_combine_daily_submissions": False,
    "submission_limit_reset_time": "00:00:00",
    "submission_limit_reset_timezone": "US/Eastern",
    "num_bonus_submissions": 0,
    "total_submission_limit": None,
    "allow_late_days": False,
    "ultimate_submission_policy": "best",
    "hide_ultimate_submission_fdbk": False,
    "instructor_files": [
        {
            "pk": 21908,
            "project": 1005,
            "name": "autograder-6f82202d.tar.gz",
            "last_modified": "2021-04-07T02:16:02.992523Z",
            "size": 11323
        },
        {
            "pk": 21909,
            "project": 1005,
            "name": "install",
            "last_modified": "2021-04-07T02:16:03.147228Z",
            "size": 2230
        }
    ],
    "expected_student_files": [
        {
            "pk": 2545,
            "project": 1005,
            "pattern": "submit.tar.gz",
            "min_num_matches": 1,
            "max_num_matches": 1,
            "last_modified": "2021-04-07T00:31:21.379258Z"
        }
    ],
    "has_handgrading_rubric": False,
    "send_email_on_submission_received": True,
    "send_email_on_non_deferred_tests_finished": True,
    "use_honor_pledge": True,
    "honor_pledge_text": (
        "I have neither given nor received aid on this project, "
        "nor have I concealed any violations of the Honor Code."
    )
}
