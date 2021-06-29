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

    # Group list
    requests_mock.get(
        "https://autograder.io/api/projects/1005/groups/",
        text=json.dumps(
            [
                {
                    "pk": 247242,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "abbansal@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 12457,
                            "username": "abbansal@umich.edu",
                            "first_name": "Ashish",
                            "last_name": "Bansal",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T15:43:14.771345Z",
                    "last_modified": "2021-05-05T15:43:14.771148Z"
                },
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
                    "pk": 247643,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "ajsaxe@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11219,
                            "username": "ajsaxe@umich.edu",
                            "first_name": "Ellie",
                            "last_name": "Saxe",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-12T00:41:42.589637Z",
                    "last_modified": "2021-05-12T00:41:42.589466Z"
                },
                {
                    "pk": 247444,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "anqiwa@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20392,
                            "username": "anqiwa@umich.edu",
                            "first_name": "Anqi",
                            "last_name": "Wang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 10,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T03:46:36.305175Z",
                    "last_modified": "2021-05-09T03:46:36.305008Z"
                },
                {
                    "pk": 247517,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "ashraj@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 21317,
                            "username": "ashraj@umich.edu",
                            "first_name": "Ashwani",
                            "last_name": "Aggarwal",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T07:13:22.997773Z",
                    "last_modified": "2021-05-10T07:13:22.997583Z"
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
                {
                    "pk": 247283,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "azshen@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15784,
                            "username": "azshen@umich.edu",
                            "first_name": "Andrew",
                            "last_name": "Shen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 9,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T01:53:30.318800Z",
                    "last_modified": "2021-05-06T01:53:30.318638Z"
                },
                {
                    "pk": 247249,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "bmcnair@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 18335,
                            "username": "bmcnair@umich.edu",
                            "first_name": "Brian",
                            "last_name": "McNair",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 5,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T17:09:23.760536Z",
                    "last_modified": "2021-05-05T17:09:23.760387Z"
                },
                {
                    "pk": 248457,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "bohanw@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 2085,
                            "username": "bohanw@umich.edu",
                            "first_name": "Bohan",
                            "last_name": "Wang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-30T04:33:43.102298Z",
                    "last_modified": "2021-05-30T04:33:43.102095Z"
                },
                {
                    "pk": 247416,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "camt@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 14997,
                            "username": "camt@umich.edu",
                            "first_name": "Cam",
                            "last_name": "Thomas",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 7,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T15:17:35.548165Z",
                    "last_modified": "2021-05-08T15:17:35.547945Z"
                },
                {
                    "pk": 247257,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "cawyman@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11409,
                            "username": "cawyman@umich.edu",
                            "first_name": "Carolyn",
                            "last_name": "Wyman",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T18:57:16.510434Z",
                    "last_modified": "2021-05-05T18:57:16.510288Z"
                },
                {
                    "pk": 247306,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "cerubins@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 18351,
                            "username": "cerubins@umich.edu",
                            "first_name": "Carlos",
                            "last_name": "Rubins",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T19:01:36.251687Z",
                    "last_modified": "2021-05-06T19:01:36.251530Z"
                },
                {
                    "pk": 247312,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "chagrady@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 3445,
                            "username": "chagrady@umich.edu",
                            "first_name": "Charles",
                            "last_name": "Grady",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T20:11:40.727556Z",
                    "last_modified": "2021-05-06T20:11:40.727391Z"
                },
                {
                    "pk": 247350,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "cjiangz@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 18309,
                            "username": "cjiangz@umich.edu",
                            "first_name": "Christopher",
                            "last_name": "Jiang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T03:29:11.879875Z",
                    "last_modified": "2021-05-07T03:29:11.879716Z"
                },
                {
                    "pk": 247349,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "cjrwill@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11598,
                            "username": "cjrwill@umich.edu",
                            "first_name": "Christopher",
                            "last_name": "Williams",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T02:45:10.139655Z",
                    "last_modified": "2021-05-07T02:45:10.139491Z"
                },
                {
                    "pk": 247391,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "comandma@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20720,
                            "username": "comandma@umich.edu",
                            "first_name": "Marco",
                            "last_name": "Comandante Lou",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 6,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T00:24:42.864968Z",
                    "last_modified": "2021-05-08T00:24:42.864807Z"
                },
                {
                    "pk": 247374,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "crein@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 2875,
                            "username": "crein@umich.edu",
                            "first_name": "Charles",
                            "last_name": "Reinertson",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T17:47:40.569066Z",
                    "last_modified": "2021-05-07T17:47:40.568874Z"
                },
                {
                    "pk": 247256,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "cwsimms@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 3755,
                            "username": "cwsimms@umich.edu",
                            "first_name": "Charles",
                            "last_name": "Simms",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T18:35:20.619349Z",
                    "last_modified": "2021-05-05T18:35:20.619165Z"
                },
                {
                    "pk": 247534,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "danchoe@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 8948,
                            "username": "danchoe@umich.edu",
                            "first_name": "Daniel",
                            "last_name": "Choe",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T19:14:43.374127Z",
                    "last_modified": "2021-05-10T19:14:43.373961Z"
                },
                {
                    "pk": 247502,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "danyaoch@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15169,
                            "username": "danyaoch@umich.edu",
                            "first_name": "Danyao",
                            "last_name": "Chen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T03:26:56.232659Z",
                    "last_modified": "2021-05-10T03:26:56.232447Z"
                },
                {
                    "pk": 247473,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "davidmey@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 5248,
                            "username": "davidmey@umich.edu",
                            "first_name": "David",
                            "last_name": "Meyer",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T19:21:21.410570Z",
                    "last_modified": "2021-05-09T19:21:21.410380Z"
                },
                {
                    "pk": 247615,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "delgizzi@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 10646,
                            "username": "delgizzi@umich.edu",
                            "first_name": "Theodore",
                            "last_name": "Delgizzi",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-11T20:13:07.893193Z",
                    "last_modified": "2021-05-11T20:13:07.892980Z"
                },
                {
                    "pk": 247492,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "dmellogu@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15228,
                            "username": "dmellogu@umich.edu",
                            "first_name": "Gustavo",
                            "last_name": "D'Mello",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T02:17:39.792364Z",
                    "last_modified": "2021-05-10T02:17:39.792174Z"
                },
                {
                    "pk": 247298,
                    "project": 1005,
                    "extended_due_date": "2021-05-13T03:59:22Z",
                    "member_names": [
                        "ejfurr@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 5279,
                            "username": "ejfurr@umich.edu",
                            "first_name": "Jordan",
                            "last_name": "Furr",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 5,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T14:55:25.951877Z",
                    "last_modified": "2021-05-11T14:49:01.459304Z"
                },
                {
                    "pk": 248390,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "gongyr@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 28809,
                            "username": "gongyr@umich.edu",
                            "first_name": "Yuru",
                            "last_name": "Gong",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-27T01:26:53.502347Z",
                    "last_modified": "2021-05-27T01:26:53.502124Z"
                },
                {
                    "pk": 247497,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "gontaryk@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 9527,
                            "username": "gontaryk@umich.edu",
                            "first_name": "John",
                            "last_name": "Gontaryk",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 5,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T03:05:56.119114Z",
                    "last_modified": "2021-05-10T03:05:56.118923Z"
                },
                {
                    "pk": 247364,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "gradtke@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 8795,
                            "username": "gradtke@umich.edu",
                            "first_name": "Graham",
                            "last_name": "Radtke",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T13:44:17.438528Z",
                    "last_modified": "2021-05-07T13:44:17.438342Z"
                },
                {
                    "pk": 247652,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "grahammt@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 2686,
                            "username": "grahammt@umich.edu",
                            "first_name": "Graham",
                            "last_name": "Tarling",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-12T02:51:32.111032Z",
                    "last_modified": "2021-05-12T02:51:32.110852Z"
                },
                {
                    "pk": 247576,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "hanchzha@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 17138,
                            "username": "hanchzha@umich.edu",
                            "first_name": "Hanchi",
                            "last_name": "Zhang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-11T03:56:58.985193Z",
                    "last_modified": "2021-05-11T03:56:58.985023Z"
                },
                {
                    "pk": 247282,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "hanyongq@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 25339,
                            "username": "hanyongq@umich.edu",
                            "first_name": "Yongqi",
                            "last_name": "Han",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T01:51:57.026040Z",
                    "last_modified": "2021-05-06T01:51:57.025831Z"
                },
                {
                    "pk": 247293,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "hbingyan@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 21321,
                            "username": "hbingyan@umich.edu",
                            "first_name": "Bingyan",
                            "last_name": "Hu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T08:30:36.651520Z",
                    "last_modified": "2021-05-06T08:30:36.651358Z"
                },
                {
                    "pk": 247313,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "hheidi@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 17013,
                            "username": "hheidi@umich.edu",
                            "first_name": "Heidi",
                            "last_name": "Huang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T20:59:28.364451Z",
                    "last_modified": "2021-05-06T20:59:28.364218Z"
                },
                {
                    "pk": 248008,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "itsandy@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 21611,
                            "username": "itsandy@umich.edu",
                            "first_name": "Andy",
                            "last_name": "Wang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-18T18:23:59.062403Z",
                    "last_modified": "2021-05-18T18:23:59.062146Z"
                },
                {
                    "pk": 243647,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jadchaar@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 862,
                            "username": "jadchaar@umich.edu",
                            "first_name": "Jad",
                            "last_name": "Chaar",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-04-07T02:49:10.517949Z",
                    "last_modified": "2021-04-07T02:49:10.517651Z"
                },
                {
                    "pk": 247235,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jeonghin@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20699,
                            "username": "jeonghin@umich.edu",
                            "first_name": "Raphael Jeong-Hin",
                            "last_name": "Chin",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T13:46:10.170000Z",
                    "last_modified": "2021-05-05T13:46:10.169829Z"
                },
                {
                    "pk": 247294,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jessasch@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 9847,
                            "username": "jessasch@umich.edu",
                            "first_name": "Jessica",
                            "last_name": "Schoonbee",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 6,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T12:03:42.861719Z",
                    "last_modified": "2021-05-06T12:03:42.861530Z"
                },
                {
                    "pk": 247205,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jmapple@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11952,
                            "username": "jmapple@umich.edu",
                            "first_name": "Justin",
                            "last_name": "Applefield",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-04T19:09:10.042936Z",
                    "last_modified": "2021-05-04T19:09:10.042790Z"
                },
                {
                    "pk": 247314,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jmcolvin@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 3361,
                            "username": "jmcolvin@umich.edu",
                            "first_name": "Jumanah",
                            "last_name": "Colvin",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T21:21:09.701003Z",
                    "last_modified": "2021-05-06T21:21:09.700766Z"
                },
                {
                    "pk": 247261,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "josepark@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11113,
                            "username": "josepark@umich.edu",
                            "first_name": "Joseph",
                            "last_name": "Park",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 6,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T19:13:58.644838Z",
                    "last_modified": "2021-05-05T19:13:58.644680Z"
                },
                {
                    "pk": 247341,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jtfaulds@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11956,
                            "username": "jtfaulds@umich.edu",
                            "first_name": "Jaron",
                            "last_name": "Faulds",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T00:34:51.279584Z",
                    "last_modified": "2021-05-07T00:34:51.279418Z"
                },
                {
                    "pk": 247453,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "junhuang@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15389,
                            "username": "junhuang@umich.edu",
                            "first_name": "Junliang",
                            "last_name": "Huang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T13:51:12.759054Z",
                    "last_modified": "2021-05-09T13:51:12.758883Z"
                },
                {
                    "pk": 247530,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "jxichen@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 28532,
                            "username": "jxichen@umich.edu",
                            "first_name": "Jiaxi",
                            "last_name": "Chen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T18:12:55.809295Z",
                    "last_modified": "2021-05-10T18:12:55.809079Z"
                },
                {
                    "pk": 247460,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "kije@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 1681,
                            "username": "kije@umich.edu",
                            "first_name": "Jack",
                            "last_name": "Thiesen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T15:58:10.394139Z",
                    "last_modified": "2021-05-09T15:58:10.393982Z"
                },
                {
                    "pk": 247448,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "kimesthe@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15455,
                            "username": "kimesthe@umich.edu",
                            "first_name": "Esther",
                            "last_name": "Kim",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T05:28:55.754698Z",
                    "last_modified": "2021-05-09T05:28:55.754492Z"
                },
                {
                    "pk": 247644,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "kshenton@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11244,
                            "username": "kshenton@umich.edu",
                            "first_name": "Kate",
                            "last_name": "Shenton",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-12T00:51:20.602569Z",
                    "last_modified": "2021-05-12T00:51:20.602389Z"
                },
                {
                    "pk": 247496,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "leyyang@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20959,
                            "username": "leyyang@umich.edu",
                            "first_name": "Leyao",
                            "last_name": "Yang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T02:52:33.437723Z",
                    "last_modified": "2021-05-10T02:52:33.437509Z"
                },
                {
                    "pk": 247445,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "lhalice@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20870,
                            "username": "lhalice@umich.edu",
                            "first_name": "Han",
                            "last_name": "Liu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T03:56:43.960898Z",
                    "last_modified": "2021-05-09T03:56:43.960683Z"
                },
                {
                    "pk": 247403,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "liuxingy@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 14901,
                            "username": "liuxingy@umich.edu",
                            "first_name": "Xingyu",
                            "last_name": "Liu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T03:20:31.586144Z",
                    "last_modified": "2021-05-08T03:20:31.586005Z"
                },
                {
                    "pk": 247439,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "luozx@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 21116,
                            "username": "luozx@umich.edu",
                            "first_name": "Zixiong",
                            "last_name": "Luo",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T02:48:51.348654Z",
                    "last_modified": "2021-05-09T02:48:51.348444Z"
                },
                {
                    "pk": 247446,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "mguastal@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 12749,
                            "username": "mguastal@umich.edu",
                            "first_name": "Michael",
                            "last_name": "Guastalla",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T04:15:08.464494Z",
                    "last_modified": "2021-05-09T04:15:08.464284Z"
                },
                {
                    "pk": 247386,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "michye@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 19516,
                            "username": "michye@umich.edu",
                            "first_name": "Michael",
                            "last_name": "Ye",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 11,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T21:53:51.928323Z",
                    "last_modified": "2021-05-07T21:53:51.928134Z"
                },
                {
                    "pk": 247385,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "mohnisha@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 16956,
                            "username": "mohnisha@umich.edu",
                            "first_name": "Mohnish",
                            "last_name": "Aggarwal",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 5,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T21:50:03.685956Z",
                    "last_modified": "2021-05-07T21:50:03.685765Z"
                },
                {
                    "pk": 247521,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "mokhatib@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11986,
                            "username": "mokhatib@umich.edu",
                            "first_name": "Mohamad",
                            "last_name": "Khatib",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T14:26:36.410483Z",
                    "last_modified": "2021-05-10T14:26:36.410240Z"
                },
                {
                    "pk": 247494,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "mscroggs@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 8755,
                            "username": "mscroggs@umich.edu",
                            "first_name": "Maxwell",
                            "last_name": "Scroggs",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T02:41:35.049327Z",
                    "last_modified": "2021-05-10T02:41:35.049161Z"
                },
                {
                    "pk": 247488,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "murphyge@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 8531,
                            "username": "murphyge@umich.edu",
                            "first_name": "Grace",
                            "last_name": "Murphy",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T00:09:53.267994Z",
                    "last_modified": "2021-05-10T00:09:53.267846Z"
                },
                {
                    "pk": 247209,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "myounus@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 4387,
                            "username": "myounus@umich.edu",
                            "first_name": "Maryam",
                            "last_name": "Younus",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-04T19:22:19.078216Z",
                    "last_modified": "2021-05-04T19:22:19.078063Z"
                },
                {
                    "pk": 247422,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "nkess@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 10877,
                            "username": "nkess@umich.edu",
                            "first_name": "Nicole",
                            "last_name": "Kessler",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 6,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T18:49:01.404976Z",
                    "last_modified": "2021-05-08T18:49:01.404793Z"
                },
                {
                    "pk": 247396,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "parthdpa@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 9192,
                            "username": "parthdpa@umich.edu",
                            "first_name": "Parth",
                            "last_name": "Patel",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T01:13:40.662374Z",
                    "last_modified": "2021-05-08T01:13:40.662172Z"
                },
                {
                    "pk": 247408,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "paulyuen@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15997,
                            "username": "paulyuen@umich.edu",
                            "first_name": "Tian",
                            "last_name": "Yuan",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T08:48:02.941942Z",
                    "last_modified": "2021-05-08T08:48:02.941777Z"
                },
                {
                    "pk": 247504,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "perper@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15954,
                            "username": "perper@umich.edu",
                            "first_name": "Tianle",
                            "last_name": "Wu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T03:45:59.622938Z",
                    "last_modified": "2021-05-10T03:45:59.622762Z"
                },
                {
                    "pk": 247609,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "ppw@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 2050,
                            "username": "ppw@umich.edu",
                            "first_name": "Parker",
                            "last_name": "Wrzesinski",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-11T19:37:17.634044Z",
                    "last_modified": "2021-05-11T19:37:17.633820Z"
                },
                {
                    "pk": 247413,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "sanketn@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 17063,
                            "username": "sanketn@umich.edu",
                            "first_name": "Sunny",
                            "last_name": "Nayak",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T10:00:51.164313Z",
                    "last_modified": "2021-05-08T10:00:51.164131Z"
                },
                {
                    "pk": 247642,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "shahwaiz@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15778,
                            "username": "shahwaiz@umich.edu",
                            "first_name": "Shahwaiz",
                            "last_name": "Shah",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-12T00:05:17.075327Z",
                    "last_modified": "2021-05-12T00:05:17.075173Z"
                },
                {
                    "pk": 247505,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "shiqy@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15793,
                            "username": "shiqy@umich.edu",
                            "first_name": "Qiuyu",
                            "last_name": "Shi",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 7,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T03:51:31.826175Z",
                    "last_modified": "2021-05-10T03:51:31.825957Z"
                },
                {
                    "pk": 247247,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "sjaemin@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 16700,
                            "username": "sjaemin@umich.edu",
                            "first_name": "Jae Min",
                            "last_name": "Shin",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T16:31:13.573618Z",
                    "last_modified": "2021-05-05T16:31:13.573427Z"
                },
                {
                    "pk": 247420,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "suhaasn@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 4248,
                            "username": "suhaasn@umich.edu",
                            "first_name": "Suhaas",
                            "last_name": "Nandyala",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T17:53:58.399040Z",
                    "last_modified": "2021-05-08T17:53:58.398871Z"
                },
                {
                    "pk": 247375,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "trym@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 18687,
                            "username": "trym@umich.edu",
                            "first_name": "Trym Augustin Honstad",
                            "last_name": "Ramberg",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T18:21:01.486750Z",
                    "last_modified": "2021-05-07T18:21:01.486533Z"
                },
                {
                    "pk": 247264,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "tvday@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15238,
                            "username": "tvday@umich.edu",
                            "first_name": "Thomas",
                            "last_name": "Day",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T20:17:42.143570Z",
                    "last_modified": "2021-05-05T20:17:42.143407Z"
                },
                {
                    "pk": 247604,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "usmanaa@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 16818,
                            "username": "usmanaa@umich.edu",
                            "first_name": "Ahmed",
                            "last_name": "Usman",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-11T19:02:34.180109Z",
                    "last_modified": "2021-05-11T19:02:34.179906Z"
                },
                {
                    "pk": 247454,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "waxinyu@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 17498,
                            "username": "waxinyu@umich.edu",
                            "first_name": "Xinyu",
                            "last_name": "Wang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T13:52:18.587616Z",
                    "last_modified": "2021-05-09T13:52:18.587471Z"
                },
                {
                    "pk": 247255,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "wrapieng@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15709,
                            "username": "wrapieng@umich.edu",
                            "first_name": "Wilbur",
                            "last_name": "Rapieng",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 3,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T18:16:30.007100Z",
                    "last_modified": "2021-05-05T18:16:30.006903Z"
                },
                {
                    "pk": 247358,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "xianglol@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15503,
                            "username": "xianglol@umich.edu",
                            "first_name": "Xianglong",
                            "last_name": "Li",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-07T09:21:18.509013Z",
                    "last_modified": "2021-05-07T09:21:18.508864Z"
                },
                {
                    "pk": 247405,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "xusksksk@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 17709,
                            "username": "xusksksk@umich.edu",
                            "first_name": "Haozhi",
                            "last_name": "Xu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 2,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T04:09:47.239712Z",
                    "last_modified": "2021-05-08T04:09:47.239499Z"
                },
                {
                    "pk": 247545,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "xytang@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20824,
                            "username": "xytang@umich.edu",
                            "first_name": "Shereen",
                            "last_name": "Tang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T22:22:57.577699Z",
                    "last_modified": "2021-05-10T22:22:57.577510Z"
                },
                {
                    "pk": 247265,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "yangfn@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 15034,
                            "username": "yangfn@umich.edu",
                            "first_name": "Frank",
                            "last_name": "Yang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 10,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-05T20:49:47.692328Z",
                    "last_modified": "2021-05-05T20:49:47.692101Z"
                },
                {
                    "pk": 247299,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "yfw@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 11363,
                            "username": "yfw@umich.edu",
                            "first_name": "Louis",
                            "last_name": "Wang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T15:17:18.538770Z",
                    "last_modified": "2021-05-06T15:17:18.538622Z"
                },
                {
                    "pk": 247490,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "ytyuting@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 16926,
                            "username": "ytyuting@umich.edu",
                            "first_name": "Yuting",
                            "last_name": "Jiang",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 5,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-10T01:11:36.198531Z",
                    "last_modified": "2021-05-10T01:11:36.198369Z"
                },
                {
                    "pk": 247328,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "yuhchen@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 18453,
                            "username": "yuhchen@umich.edu",
                            "first_name": "Yuhong",
                            "last_name": "Chen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-06T23:26:25.187841Z",
                    "last_modified": "2021-05-06T23:26:25.187694Z"
                },
                {
                    "pk": 247449,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "yyassine@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 20717,
                            "username": "yyassine@umich.edu",
                            "first_name": "Yasser",
                            "last_name": "Yassine",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 1,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-09T06:10:08.431885Z",
                    "last_modified": "2021-05-09T06:10:08.431719Z"
                },
                {
                    "pk": 247560,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "zhuoyzhu@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 16043,
                            "username": "zhuoyzhu@umich.edu",
                            "first_name": "Zhuoyu",
                            "last_name": "Zhu",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 4,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-11T01:50:37.460193Z",
                    "last_modified": "2021-05-11T01:50:37.459977Z"
                },
                {
                    "pk": 247651,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "zixiangz@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 21647,
                            "username": "zixiangz@umich.edu",
                            "first_name": "Zixiang",
                            "last_name": "Zhou",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 0,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-12T02:27:24.362175Z",
                    "last_modified": "2021-05-12T02:27:24.361939Z"
                },
                {
                    "pk": 247406,
                    "project": 1005,
                    "extended_due_date": None,
                    "member_names": [
                        "ziyanc@umich.edu"
                    ],
                    "members": [
                        {
                            "pk": 26422,
                            "username": "ziyanc@umich.edu",
                            "first_name": "Jerry",
                            "last_name": "Chen",
                            "email": "",
                            "is_superuser": False
                        }
                    ],
                    "bonus_submissions_remaining": 0,
                    "late_days_used": {},
                    "num_submissions": 6,
                    "num_submits_towards_limit": 0,
                    "created_at": "2021-05-08T05:03:54.264177Z",
                    "last_modified": "2021-05-08T05:03:54.263946Z"
                }
            ]),
    )

    # Group detai
    requests_mock.get(
        "https://autograder.io/api/groups/246965/",
        text=json.dumps(GROUP_246965),
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


GROUP_246965 = {
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
}
