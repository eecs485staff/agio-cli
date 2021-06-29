"""Common utility functions."""
import datetime as dt
import json
import sys
import re
import pick


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
    """Return a tuple for sorting courses by year, semester, and name."""
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


def course_match(search, courses):
    """Given a search term, return the best matching course or None."""
    year, semester, name = parse_course_string(search)
    courses = filter(
        lambda x:
            x["year"] == year and
            x["semester"] == semester and
            name in x["name"],
        courses
    )

    # If there's only 1 course, return that
    courses = list(courses)
    if not courses:
        return None
    if len(courses) == 1:
        return courses[0]
    sys.exit(f"Error: more than one course matches '{search}': {courses}")


def print_dict(obj):
    """Pretty print a dictionary."""
    print(json.dumps(obj, indent=4))


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
    (?P<sem>                    # Semester name or abbreviation
        w|wn|winter|
        sp|s|spring|
        su|summer|
        sp/su|spsu|ss|spring/summer|
        f|fa|fall)
    \s*                         # Optional whitespace
    (?P<year>\d{2,4})           # 2-4 digit year
    \s*                         # Optional whitespace
    $                           # Match ends at the end
    """
    match = re.search(pattern, user_input, re.IGNORECASE)
    if not match:
        print("Error: unsupported input format")
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
        "s": "Spring",
        "spring": "Spring",
        "su": "Summer",
        "summer": "Summer",
        "sp/su": "Spring/Summer",
        "spsu": "Spring/Summer",
        "ss": "Spring/Summer",
        "spring/summer": "Spring/Summer",
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


def get_current_course_list(client):
    """Return a sorted list of current and future courses."""
    user = client.get("/api/users/current/")
    courses = client.get(f"/api/users/{user['pk']}/courses_is_admin_for/")
    courses = sorted(courses, key=course_key, reverse=True)
    return courses


def get_course_smart(course_arg, client):
    # User provides course PK
    if course_arg and course_arg.isnumeric():
        return client.get(f"/api/courses/{course_arg}/")

    # Get a list of courses sorted by year, semester and name
    courses = get_current_course_list(client)

    # No course input from the user.  Filter for current courses, and them
    # prompt the user.  If there's only one, then don't bother to prompt.
    if not course_arg:
        courses = list(filter(is_current_course, courses))
        if not courses:
            # FIXME raise exception
            sys.exit("Error: No current courses, try 'agio courses -l'")
        elif len(courses) == 1:
            return courses[0]
        else:
            selected_courses = pick.pick(
                options=courses,
                title=("Select a course:"),
                options_map_func=lambda x:
                    f"{x['name']} {x['semester']} {x['year']}",
                multiselect=False,
            )
            assert selected_courses
            return selected_courses[0]

    # Try to match a course
    match = course_match(course_arg, courses)
    if not match:
        # FIXME raise exception
        print(f"Error: couldn't find a course matching '{course_arg}'")
        for i in courses:
            print(f"[{i['pk']}]\t{i['name']} {i['semester']} {i['year']}")
        sys.exit(1)
    return match


def parse_project_string(user_input):
    """Return title, subtitle from a user input string.

    EXAMPLE:
    >>> parse_course_string("p4mapreduce")
    ('Project', 4, 'mapreduce')
    """

    if user_input[0].isdigit() or user_input.lower().startswith('p'):
        type = "Project"
    elif user_input.lower().startswith('l'):
        type = "Lab"
    elif user_input.lower().startswith('h'):
        type = "Homework"
    else:
        print("Error: unsupported input format")
        return None, None

    pattern = r"""(?ix)         # Regex options: case insensitive, verbose
    ^
    \D*
    (?P<num>\d*)                # Assignment number
    \W*                         # Optional whitespace/delimeters
    (?P<name>[\w\s]*)           # Assignment name
    \s*                         # Optional whitespace
    $                           # Match ends at the end
    """

    match = re.search(pattern, user_input, re.IGNORECASE)
    if not match:
        print("Error: unsupported input format")
        return None, None

    num = int(match.group("num"))
    name = match.group("name")
    if type == "Project":
        return f"{type} {num}", name
    else:
        return f"{type} {num:02d}", name


def project_match(search, projects):
    """Given a search term, return the best matching project or None."""
    title, subtitle = parse_project_string(search)
    projects = filter(
        lambda x:
            x["name"].startswith(title) and
            subtitle.lower().replace(
                " ", "") in x["name"].lower().replace(" ", ""),
        projects
    )
    projects = list(projects)
    if not projects:
        return None
    if len(projects) == 1:
        return projects[0]
    sys.exit(f"Error: more than one project matches '{search}': {projects}")


def get_course_project_list(course, client):
    """Return a sorted list of projects for course."""
    projects = client.get(f"/api/courses/{course['pk']}/projects/")
    projects = sorted(projects, key=lambda x: x["name"])
    return projects


def get_project_smart(project_arg, course_arg, client):
    # User provides project PK
    if project_arg and project_arg.isnumeric():
        return client.get(f"/api/projects/{project_arg}/")

    # Get a course
    course = get_course_smart(course_arg, client)

    # Get a list of projects for this course, sorted by name
    project_list = client.get(f"/api/courses/{course['pk']}/projects/")
    project_list = sorted(project_list, key=lambda x: x["name"])
    if not project_list:
        # FIXME throw exception
        sys.exit("Error: No projects for course, try 'agio courses -l'")

    # No project input from the user.  Show all projects for current course and
    # and prompt the user.
    if not project_arg:
        selected_projects = pick.pick(
            options=project_list,
            title="Select a project:",
            options_map_func=lambda x: f"{x['name']}",
            multiselect=False,
        )
        assert selected_projects
        return selected_projects[0]

    # User provides strings, try to match a project
    match = project_match(project_arg, project_list)
    if not match:
        print(f"Error: couldn't find a project matching '{project_arg}'")
        # FIXME copy pasta
        for i in project_list:
            print(f"[{i['pk']}]\t{i['name']}")
        sys.exit(1)
    return match


def group_uniqnames(group):
    """Return a list of uniqnames who are members of group."""
    members = group["members"]
    return [x["username"].replace("@umich.edu", "") for x in members]


def group_str(group):
    """Format group as string."""
    uniqnames = group_uniqnames(group)
    uniqnames_str = ", ".join(uniqnames)
    return f"[{group['pk']}] {uniqnames_str}"


def is_group_member(uniqname, group):
    """Return True if uniqname is in group."""
    return uniqname in group_uniqnames(group)


def group_match(uniqname, groups):
    """Return group where uniqname is a member."""
    matches = filter(lambda x: is_group_member(uniqname, x), groups)
    return list(matches)


def get_group_list(project, client):
    groups = client.get(f"/api/projects/{project['pk']}/groups/")
    groups = sorted(groups, key=lambda x: x["pk"])
    return groups


def get_group_smart(group_arg, project_arg, course_arg, client):
    # User provides group PK
    if group_arg and group_arg.isnumeric():
        return client.get(f"/api/groups/{group_arg}/")

    # Get a project and list of groups
    project = get_project_smart(project_arg, course_arg, client)
    group_list = get_group_list(project, client)

    # No group input from the user.  Show all groups for selected project and
    # and prompt the user.
    if not group_arg:
        selected_groups = pick.pick(
            options=group_list,
            title="Select a group:",
            options_map_func=group_str,
            multiselect=False,
        )
        assert selected_groups
        return selected_groups[0]

    # # If the user provides a uniqname, look it up
    # if not group_arg.isnumeric():
    #     uniqname = group_pk_or_uniqname
    #     group_list = client.get(f"/api/projects/{project_pk}/groups/")
    #     group = utils.find_group(uniqname, group_list)
    #     group_pk = group["pk"]
    # else:
    #     group_pk = group_pk_or_uniqname[0]


    # User provides strings, try to match a group
    matches = group_match(group_arg, group_list)
    if not matches:
        print(f"Error: uniqname not in any group: {group_arg}")
        for i in group_list:
            print(group_str(i))
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: uniqname in more than one group: {group_arg}")
        sys.exit(1)
    return matches[0]
