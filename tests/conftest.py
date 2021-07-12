"""Shared test fixtures."""
import json
import pytest


@pytest.fixture(name="constants")
def constants_setup():
    """Global constants."""
    return {
        "COURSE_109": {
            "pk": 109,
            "name": "EECS 485",
            "semester": "Spring",
            "year": 2021,
            "subtitle": "Web Systems",
            "num_late_days": 0,
            "allowed_guest_domain": "@umich.edu",
            "last_modified": "2021-04-07T02:19:22.818992Z"
        },
        "PROJECT_1005": {
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
        },
        "GROUP_246965": {
            "pk": 246965,
            "project": 1005,
            "extended_due_date": None,
            "member_names": [
                "awdeorio@umich.edu"
            ],
            "members": [
                {
                    "pk": 5,
                    "username": "awdeorio@umich.edu",
                    "first_name": "Andrew",
                    "last_name": "DeOrio",
                    "email": "",
                    "is_superuser": False
                }
            ],
            "bonus_submissions_remaining": 0,
            "late_days_used": {},
            "num_submissions": 2,
            "num_submits_towards_limit": 1,
            "created_at": "2021-04-21T17:01:37.807261Z",
            "last_modified": "2021-04-21T17:01:37.807025Z"
        },
        "SUBMISSION_1128572": {
            "pk": 1128572,
            "group": 246965,
            "timestamp": "2021-06-29T14:55:57.886137Z",
            "submitter": "awdeorio@umich.edu",
            "submitted_filenames": [
                "submit.tar.gz"
            ],
            "discarded_files": [],
            "missing_files": {},
            "status": "finished_grading",
            "is_past_daily_limit": False,
            "is_bonus_submission": False,
            "count_towards_total_limit": True,
            "does_not_count_for": [],
            "position_in_queue": 0,
            "grading_start_time": "2021-06-29T14:56:04.154353Z",
            "non_deferred_grading_end_time": "2021-06-29T14:56:56.289720Z",
            "last_modified": "2021-06-29T14:56:55.378590Z"
        },
        "SUBMISSION_1125717": {
            "pk": 1125717,
            "group": 246965,
            "timestamp": "2021-06-09T12:49:16.047791Z",
            "submitter": "awdeorio@umich.edu",
            "submitted_filenames": [
                "submit.tar.gz"
            ],
            "discarded_files": [],
            "missing_files": {},
            "status": "finished_grading",
            "is_past_daily_limit": False,
            "is_bonus_submission": False,
            "count_towards_total_limit": True,
            "does_not_count_for": [],
            "position_in_queue": 0,
            "grading_start_time": "2021-06-09T12:49:21.340598Z",
            "non_deferred_grading_end_time": "2021-06-09T12:50:26.978440Z",
            "last_modified": "2021-06-09T12:50:25.899462Z"
        }
    }


@pytest.fixture(name="api_mock")
def api_requests_mock(requests_mock, mocker, constants):
    """Mock Autograder API with hardcoded responses."""
    # Don't look for an API token on the filesystem
    mocker.patch("agiocli.api_client.get_api_token")

    # User
    requests_mock.get(
        "https://autograder.io/api/users/current/",
        headers={"Content-Type": "application/json"},
        text=json.dumps({
            "pk": 5,
            "username": "awdeorio@umich.edu",
            "first_name": "Andrew",
            "last_name": "DeOrio",
            "email": "",
            "is_superuser": False
        })
    )

    # Course list / admin
    requests_mock.get(
        "https://autograder.io/api/users/5/courses_is_admin_for/",
        headers={"Content-Type": "application/json"},
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
            constants["COURSE_109"],
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

    # Course list / staff
    requests_mock.get(
        "https://autograder.io/api/users/5/courses_is_staff_for/",
        headers={"Content-Type": "application/json"},
        text=json.dumps([
            {
                "pk": 1,
                "name": "EECS 280",
                "semester": "Fall",
                "year": 2016,
                "subtitle": "",
                "num_late_days": 0,
                "allowed_guest_domain": "@umich.edu",
                "last_modified": "2019-02-07T21:06:01.779838Z"
            },
        ])
    )

    # Course detail
    requests_mock.get(
        "https://autograder.io/api/courses/109/",
        headers={"Content-Type": "application/json"},
        text=json.dumps(constants["COURSE_109"]),
    )

    # Project list
    requests_mock.get(
        "https://autograder.io/api/courses/109/projects/",
        headers={"Content-Type": "application/json"},
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
            constants["PROJECT_1005"],
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
        headers={"Content-Type": "application/json"},
        text=json.dumps(constants["PROJECT_1005"]),
    )

    # Group list
    requests_mock.get(
        "https://autograder.io/api/projects/1005/groups/",
        headers={"Content-Type": "application/json"},
        text=json.dumps(
            [
                {
                    "pk": 243636,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "achitta@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11854,
                            "username": "achitta@umich.edu",
                            "first_name": "Aditya",
                            "last_name": "Chitta",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-04-07T02:17:16.975983Z",
                    "last_modified": "2021-04-07T02:17:16.975700Z"
                },
                {
                    "pk": 246965,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "awdeorio@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 5,
                            "username": "awdeorio@umich.edu",
                            "first_name": "Andrew",
                            "last_name": "DeOrio",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 1,
                    "created_at": "2021-04-21T17:01:37.807261Z",
                    "last_modified": "2021-04-21T17:01:37.807025Z"
                },
            ]),
    )

    # Group detail
    requests_mock.get(
        "https://autograder.io/api/groups/246965/",
        headers={"Content-Type": "application/json"},
        text=json.dumps(constants["GROUP_246965"]),
    )

    # Submission list
    requests_mock.get(
        "https://autograder.io/api/groups/246965/submissions/",
        headers={"Content-Type": "application/json"},
        text=json.dumps([
            constants["SUBMISSION_1128572"],
            constants["SUBMISSION_1125717"],
        ])
    )

    # Submission detail
    requests_mock.get(
        "https://autograder.io/api/submissions/1128572/",
        headers={"Content-Type": "application/json"},
        text=json.dumps(constants["SUBMISSION_1128572"]),
    )

    # Ultimate submission detail
    requests_mock.get(
        "https://autograder.io/api/groups/246965/ultimate_submission/",
        headers={"Content-Type": "application/json"},
        text=json.dumps(constants["SUBMISSION_1125717"]),
    )
