"""Common utility functions."""
import datetime as dt
import json
import sys
import re


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


def course_match(search, courses):
    """Given a search term, return the best matching course or None."""
    year, semester, name = parse_course_string(search)
    courses = filter(
        lambda x: \
            x["year"] == year and \
            x["semester"] == semester and \
            x["name"] == name,
        courses
    )

    # If there's only 1 course, return that
    courses = list(courses)
    if not courses:
        return None
    if len(courses) == 1:
        return courses[0]
    sys.exit(f"Error: more than one course matches '{search}': {courses}")


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


def parse_course_string(user_input):
    """Return year, semester, and course name from a user input string.

    EXAMPLE:
    >>> parse_course_string("eecs485sp21")
    (2021, 'Spring', 'EECS 485')
    """
    pattern = r"""(?ix)         # Regex options: case insensitive, verbose
    ^                           # Match starts at beginning
    \s*                         # Optional whitespace
    (?P<dept>[a-z]*)            # Optional department
    \s*                         # Optional whitespace
    (?P<num>\d{3})              # 3 digit course number
    \s*                         # Optional whitespace
    (?P<sem>w|wn|winter|sp|spring|su|summer|s|spring/summer|sp/su|spsu|ss|f|fa|fall)  # Semester name or abbreviation
    \s*                         # Optional whitespace
    (?P<year>\d{2,4})           # 2-4 digit year
    \s*                         # Optional whitespace
    $                           # Match ends at the end
    """
    match = re.search(pattern, user_input, re.IGNORECASE)
    if not match:
        return None, None, None

    # Convert year to a number, handling 2-digit year as "20xx"
    year = int(match.group("year"))
    assert year >= 0
    if year < 100:
        year = 2000 + year

    # Convert semester abbreviation to semester name.  Make sure that the keys
    # match the abbreviations in the regular expression above.
    semester_names = {
        "w": "Winter",
        "wn": "Winter",
        "winter": "Winter",
        "sp": "Spring",
        "su": "Spring",
        "spring": "Spring",
        "s": "Spring/Summer",
        "sp/su": "Spring/Summer",
        "spsu": "Spring/Summer",
        "ss": "Spring/Summer",
        "f": "Fall",
        "fa": "Fall",
        "fall": "Fall",
    }
    semester_abbrev = match.group("sem").lower()
    semester = semester_names[semester_abbrev]

    # Course name, with department and catalog number.  If no department is
    # specified, assume "EECS".
    dept = match.group("dept")
    dept = dept.upper()
    if not dept:
        print("WARNING: no department specified, assuming 'EECS'")
        dept = "EECS"
    num = match.group("num")
    name = f"{dept} {num}"

    # Return a tuple
    return year, semester, name
