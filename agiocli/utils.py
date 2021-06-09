"""Common utility functions."""
import datetime as dt
import difflib
import json
import sys


# Map semester name to number
SEMESTER_NUM = {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}

# Map month number to semester number
MONTH_SEMESTER_NUM = {
    1: 1, 2: 1, 3: 1, 4: 1,     # Jan-Apr Winter
    5: 2, 6: 2,                 # May-Jun Spring
    7: 3, 8: 3,                 # Jul-Aug Summer
    9: 4, 10: 4, 11: 4, 12: 4,  # Sep-Dec Fall
}


def course_key(course):
    """Return a tuple for sorting courses by year, then semester."""
    # Coerce year
    if course["year"] is None:
        year = 0
    else:
        year = course["year"]

    # Convert semester to a number
    if course["semester"] is None:
        semester_num = 0
    else:
        semester_num = SEMESTER_NUM[course["semester"]]

    # Coerce name
    name = course["name"]
    if name is None:
        name = ""

    # Return a tuple in order of sort precedence
    return (year, semester_num, name)


def is_current_course(course):
    """Return True if course is from current or future semester."""
    # Coerce year
    if course["year"] is None:
        year = 0
    else:
        year = course["year"]

    # Convert semester to a number
    if course["semester"] is None:
        semester_num = 0
    else:
        semester_num = SEMESTER_NUM[course["semester"]]

    # Compare course year and semester to today
    today = dt.date.today()
    return (
        year >= today.year and
        semester_num >= MONTH_SEMESTER_NUM[today.month]
    )


def filter_courses(courses, all_semesters=False):
    """Filter out old courses and return a sorted list."""
    if not all_semesters:
        courses = filter(is_current_course, courses)
    courses = sorted(courses, key=course_key)
    return courses


def print_course(course):
    """Print course to stdout."""
    print(
        f"[{course['pk']}] {course['name']} "
        f"{course['semester']} {course['year']}"
    )

def print_dict(obj):
    """Pretty print a dictionary."""
    print(json.dumps(obj, indent=4))


def group_uniqnames(group):
    """Return a list of uniqnames who are members of group."""
    members = group["members"]
    return [x["username"].replace("@umich.edu", "") for x in members]


def print_group(group):
    """Print one group."""
    uniqnames = group_uniqnames(group)
    uniqnames_str = ", ".join(uniqnames)
    print(f"[{group['pk']}] {uniqnames_str}")


def is_group_member(uniqname, group):
    """Return True if uniqname is in group."""
    return uniqname in group_uniqnames(group)


def find_group(uniqname, groups):
    """Return group where uniqname is a member."""
    matches = filter(lambda x: is_group_member(uniqname, x), groups)
    matches = list(matches)
    if not matches:
        sys.exit(f"Error: uniqname not in any group: {uniqname}")
    if len(matches) > 1:
        sys.exit(f"Error: uniqname in more than one group: {uniqname}")
    return matches[0]


def get_close_matches(word, possibilities, strfunc, *args, **kwargs):
    """Return a subset of possibilities matching word.

    A wrapper around difflib.get_close_matches(), extending it work on
    arbitrary objects and providing case-insensitive search.

    References:
    https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
    https://stackoverflow.com/questions/11384714/ignore-case-with-difflib-get-close-matches
    """
    # Convert each object to a string.  Each key is a string that will be
    # matched against the user-provided search word.  Each value is a reference
    # to the original object.  We also convert to lower case for
    # case-insensitive matching.
    targets = {strfunc(x).lower(): x for x in possibilities}

    # Case insensitive search term
    word = word.lower()

    # Call difflib for the match
    results = difflib.get_close_matches(word, targets.keys(), *args, **kwargs)

    # Look up difflib's result to get the corresponding original object
    match_courses = [targets[x] for x in results]
    return match_courses
