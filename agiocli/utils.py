"""Common utility functions."""
import datetime as dt
import json
import pathlib
import sys
import itertools
import re
import dateutil.parser
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


def dict_str(obj):
    """Pretty print a dictionary."""
    return json.dumps(obj, indent=4)


def course_str(course):
    """Format course as a string."""
    return (
        f"[{course['pk']}]\t{course['name']} "
        f"{course['semester']} {course['year']}"
    )


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
    """Return courses matching search term."""
    year, semester, name = parse_course_string(search)
    courses = filter(
        lambda x:
            x["year"] == year and
            x["semester"] == semester and
            name in x["name"],
        courses
    )
    return list(courses)


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
    courses += client.get(f"/api/users/{user['pk']}/courses_is_staff_for/")
    courses = sorted(courses, key=course_key, reverse=True)
    courses = [k for k,v in itertools.groupby(courses)]  # Unique
    return courses


def get_course_smart(course_arg, client):
    """Interact with the user to select a course.

    1. If course_arg is a number, look up course by primary key
    2. If course_arg is None, prompt with a list of current or futures courses
    3. If course_arg is a string, try to extract semester, year and name, then
       match against list of courses for which user is an admin.

    This function provides sanity checks and may exit with an error message.
    """
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
    matches = course_match(course_arg, courses)
    if not matches:
        print(f"Error: no course matches '{course_arg}'")
        for i in courses:
            print(course_str(i))
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Error: multiple courses match '{course_arg}'")
        for i in matches:
            print(course_str(i))
        sys.exit(1)
    return matches[0]


def parse_project_string(user_input):
    """Return assignment type, number and name from a user input string.

    EXAMPLE:
    >>> parse_project_string("p4mapreduce")
    ('Project', 4, 'mapreduce')
    """
    if user_input[0].isdigit() or user_input.lower().startswith('p'):
        assignment_type = "Project"
    elif user_input.lower().startswith('l'):
        assignment_type = "Lab"
    elif user_input.lower().startswith('h'):
        assignment_type = "Homework"
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
    if assignment_type == "Project":
        return f"{assignment_type} {num}", name
    return f"{assignment_type} {num:02d}", name


def project_str(project):
    """Format project as a string."""
    return f"[{project['pk']}]\t{project['name']}"


def project_match(search, projects):
    """Return projects matching search term."""
    title, subtitle = parse_project_string(search)
    projects = filter(
        lambda x:
            x["name"].startswith(title) and
            subtitle.lower().replace(
                " ", "") in x["name"].lower().replace(" ", ""),
        projects
    )
    return list(projects)


def get_course_project_list(course, client):
    """Return a sorted list of projects for course."""
    projects = client.get(f"/api/courses/{course['pk']}/projects/")
    projects = sorted(projects, key=lambda x: x["name"])
    return projects


def get_project_smart(project_arg, course_arg, client):
    """Interact with the user to select a project.

    1. If project_arg is a number, look up project by primary key
    2. Use previously defined procedure for smart course selection
    3. If project_arg is None, prompt with list of projects for selected course
    4. If project_arg is a string, try to match project name

    This function provides sanity checks and may exit with an error message.
    """
    # User provides project PK
    if project_arg and project_arg.isnumeric():
        return client.get(f"/api/projects/{project_arg}/")

    # Get a course
    course = get_course_smart(course_arg, client)
    assert course

    # Get a list of projects for this course, sorted by name
    projects = client.get(f"/api/courses/{course['pk']}/projects/")
    projects = sorted(projects, key=lambda x: x["name"])
    if not projects:
        sys.exit("Error: No projects for course, try 'agio courses -l'")

    # No project input from the user.  Show all projects for current course and
    # and prompt the user.
    if not project_arg:
        selected_projects = pick.pick(
            options=projects,
            title="Select a project:",
            options_map_func=lambda x: f"{x['name']}",
            multiselect=False,
        )
        assert selected_projects
        return selected_projects[0]

    # User provides strings, try to match a project
    matches = project_match(project_arg, projects)
    if not matches:
        print(f"Error: no project matches '{project_arg}'")
        for i in projects:
            print(project_str(i))
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Error: multiple projects match '{project_arg}'")
        for i in matches:
            print(project_str(i))
        sys.exit(1)
    return matches[0]


def group_str(group):
    """Format group as string."""
    uniqnames = group_uniqnames(group)
    uniqnames_str = ", ".join(uniqnames)
    return f"[{group['pk']}] {uniqnames_str}"


def group_uniqnames(group):
    """Return group member uniqnames."""
    members = group["members"]
    return [x["username"].replace("@umich.edu", "") for x in members]


def is_group_member(uniqname, group):
    """Return True if uniqname is in group."""
    return uniqname in group_uniqnames(group)


def group_match(uniqname, groups):
    """Return groups where uniqname is a member."""
    matches = filter(lambda x: is_group_member(uniqname, x), groups)
    return list(matches)


def get_group_list(project, client):
    """Return a sorted list of groups for project."""
    groups = client.get(f"/api/projects/{project['pk']}/groups/")
    groups = sorted(groups, key=lambda x: x["pk"])
    return groups


def get_group_smart(group_arg, project_arg, course_arg, client):
    """Interact with the user to select a group.

    1. If group_arg is a number, look up group by primary key
    2. Use previously defined procedure for smart project selection, which in
       turn may use the smart course selection procedure.
    3. If group_arg is None, prompt with list of groups for selected project
    4. If group_arg is a string, try to match it to a group member uniqname

    This function provides sanity checks and may exit with an error message.
    """
    # User provides group PK
    if group_arg and group_arg.isnumeric():
        return client.get(f"/api/groups/{group_arg}/")

    # Get a project and list of groups
    project = get_project_smart(project_arg, course_arg, client)
    groups = get_group_list(project, client)
    if not groups:
        sys.exit("Error: No groups for project, try 'agio projects -l'")

    # No group input from the user.  Show all groups for selected project and
    # and prompt the user.
    if not group_arg:
        selected_groups = pick.pick(
            options=groups,
            title="Select a group:",
            options_map_func=group_str,
            multiselect=False,
        )
        assert selected_groups
        return selected_groups[0]

    # User provides strings, try to match a group
    matches = group_match(group_arg, groups)
    if not matches:
        print(f"Error: uniqname not in any group: {group_arg}")
        for i in groups:
            print(group_str(i))
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Error: uniqname in more than one group: {group_arg}")
        for i in matches:
            print(group_str(i))
        sys.exit(1)
    return matches[0]


def submission_key(submission):
    """Return a tuple for sorting submissions by timestamp."""
    return dateutil.parser.parse(submission["timestamp"])


def submission_str(submission):
    """Format submission as a string."""
    timestamp = dateutil.parser.parse(submission["timestamp"])
    timestamp_human = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"[{submission['pk']}] {timestamp_human}  "
    )


def get_submission_list(group, client):
    """Return a sorted list of submissions for a group."""
    submissions = client.get(f"/api/groups/{group['pk']}/submissions/")
    submissions = sorted(submissions, key=submission_key)
    return submissions


def get_submission_smart(
        submission_arg, group_arg, project_arg, course_arg, client):
    """Interact with the user to select a submission.

    1. If submission_arg is a number, look up submission by primary key
    2. Return most recent submission

    This function provides sanity checks and may exit with an error message.
    """
    # User provides submission PK
    if submission_arg and submission_arg.isnumeric():
        return client.get(f"/api/submissions/{submission_arg}/")

    # Get a group and a list of submissions
    group = get_group_smart(group_arg, project_arg, course_arg, client)
    submissions = get_submission_list(group, client)
    if not submissions:
        sys.exit("Error: No submissions, try 'agio submissions -l'")

    # Return most recent submission
    return submissions[-1]


def download_submission(submission, group_arg, client):
    """Download the submission files.

    If there's one file, download it.  If there are multiple, then download to
    a directory.

    """
    # If the user provides a group argument like a uniqname or group pk, prefix
    # the filename with it.
    if group_arg:
        prefix = f"{group_arg}-submission-{submission['pk']}"
    else:
        prefix = f"submission-{submission['pk']}"

    # Download file to PWD.  If there are multiple files, put them in a new
    # directory.
    filenames = submission['submitted_filenames']
    if not filenames:
        print("Error: no files to download for submission")
        print(submission_str(submission))
        sys.exit(1)
    elif len(filenames) == 1:
        filename = filenames[0]
        target = pathlib.Path(f"{prefix}-{filename}")
        download_file(filename, submission, target, client)
    else:
        dirname = pathlib.Path(prefix)
        if dirname.exists():
            sys.exit(f"Error: refuse to clobber directory: {dirname}")
        dirname.mkdir()
        for filename in filenames:
            download_file(filename, submission, dirname/filename, client)


def download_file(filename, submission, target, client):
    """Download the file named filename from submission pk submission.

    Save the file in path target/filename.
    """
    if target.exists():
        sys.exit(f"Error: refuse to clobber file: {target}")
    url = f"/api/submissions/{submission['pk']}/file/?filename={filename}"
    data = client.get(url)
    with target.open("wb") as targetfile:
        targetfile.write(data)
    print(f"Saved {target}")
