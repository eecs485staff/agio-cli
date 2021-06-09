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


def get_close_matches(term, objs, keyfunc):
    # Build search target strings with name, semester and year.  Convert case
    # for case-insensitive search.  We need a dictionary so that we can
    # retrieve the original object from the search results.  For example: 'eecs
    # 280 spring 2018', 'eecs 485 winter 2019'
    targets = {keyfunc(x).lower(): x for x in objs}

    # Case insensitive search term
    term = term.lower()

    # difflib does the match
    # https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
    results = difflib.get_close_matches(term, targets.keys(), n=1)

    # Results are search target strings (see above).  Convert search target
    # string to course object.
    match_courses = [targets[x] for x in results]
    return match_courses
