"""Common utility functions."""
import datetime as dt
import difflib
import json
import sys
import re


# Map semester name to number
SEMESTER_NUM = {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}

# Map semester number to name
SEMESTER_NAME = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}

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
    course_in = transform_course_input(search)
    matches = get_close_matches(
        course_in,
        courses,
        strfunc=lambda x: f"{x['name']} {x['semester']} {x['year']}",
    )
    return matches[0] if matches else None


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


def split_digits(course_input):
    """Split string between digit and alphabetical groups."""
    return list(filter(None, re.split(r'(\d+)', course_input)))


def letter_to_term(letter):
    """Normalize term names by first letter(s)."""
    if letter[0].lower() == 'w':
        return "Winter"
    if letter[0].lower() == 'f':
        return "Fall"
    if len(letter) == 1 or letter[1].lower() == 'p':
        return "Spring"
    if letter[1].lower() == 'u':
        return "Summer"
    return ""


def four_digit_year(year):
    """Convert two-digit year into four-digit year."""
    if len(year) == 2:
        return int(f"20{year}")
    return int(year)


def transform_course_input(course_input):
    """Transform set course inputs to improve difflib matching."""

    parsed = split_digits(course_input)

    # eecs485
    if re.match(r"^[A-Za-z]+\d+$", course_input):
        # Term not provided, assume current term
        today = dt.date.today()
        current_term = f"{SEMESTER_NAME[MONTH_SEMESTER_NUM[today.month]]} {today.year}"
        return f"{parsed[0].upper()} {parsed[1]} {current_term}"

    # eecs485s21
    if re.match(r"^[A-Za-z]+\d+[A-Za-z]+\d+$", course_input):
        return (
            f"{parsed[0].upper()} {parsed[1]} "
            f"{letter_to_term(parsed[2])} {four_digit_year(parsed[3])}"
        )

    # 485s21
    if re.match(r"^\d+[A-Za-z]+\d+$", course_input):
        return (
            f"EECS {parsed[0]} "
            f"{letter_to_term(parsed[1])} {four_digit_year(parsed[2])}"
        )

    return course_input


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



def find_course_filter(course_in, course_list):
    """Procedurally filter courses from course list."""

    # If there's only 1 course, return that
    if len(course_list) == 1:
        return course_list[0]
    elif len(course_list) == 0:
        return None

    # The first number should be interpreted as the course code
    # Everything after the first number should be interpreted as the term
    # Everything before the first number should be interpreted as the department

    # Extract the course and the term (optional) from input
    course, *semester = list(filter(None, re.split(r'(\D*\d+)', course_in)))
    semester = semester[0] if semester else None

    # Split department name and course code
    if course.isnumeric():
        department = None
        course_code = course
    else:
        department, course_code = list(filter(None, re.split(r'(\d+)', course)))
    
    # Filter by course name
    if department:
        course_list = list(filter(lambda x: department.lower() in\
            x["name"].lower(), course_list))
    course_list = list(filter(lambda x: course_code in x["name"], course_list))

    # If there's only 1 course, return that
    if len(course_list) == 1:
        return course_list[0]
    elif len(course_list) == 0:
        return None

    # Split term and year
    today = dt.date.today()
    if not semester:
        # TODO: if semester not provided, should it just be the most recent
        # occurance of that class?
        term = SEMESTER_NAME[MONTH_SEMESTER_NUM[today.month]]
        year = today.year
    else:
        term, *year = list(filter(None, re.split(r'(\D+)', semester)))
        year = year[0] if year else None
        term = letter_to_term(term)
        if year:
            year = four_digit_year(year)
        else:
            # TODO: if year not provided, should it just be the most recent
            # occurance of that term?
            year = today.year

    # Filter by semester
    if year:
        course_list = list(filter(lambda x: x["year"] == year, course_list))
    course_list = list(filter(lambda x: x["semester"] == term, course_list))
    # FIXME: 's' input as summer will fail here

    # Filtering complete here
    if len(course_list) == 1:
        return course_list[0]
    elif len(course_list) == 0:
        return None
    print("FIXME: Found more than one match")
    return None
