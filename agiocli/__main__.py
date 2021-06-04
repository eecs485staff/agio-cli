"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import datetime as dt
import json
import sys
import click
from agiocli import APIClient


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-d", "--debug", is_flag=True, help="Debug output")
@click.option("-a", "--all", "all_semesters", is_flag=True,
              help="Do not filter out old semesters")
@click.pass_context
def main(ctx, debug, all_semesters):
    """Autograder.io command line interface."""
    # Pass global flags to subcommands via Click context
    # https://click.palletsprojects.com/en/latest/commands/#nested-handling-and-contexts
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    ctx.obj["ALL_SEMESTERS"] = all_semesters


@main.command()
@click.pass_context
def login(ctx):
    """Show current authenticated user."""
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    user = client.get("/api/users/current/")
    print(f"{user['username']} {user['first_name']} {user['last_name']}")


# Map semester name to number
SEMESTER_NUM = {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}

# Map month number to semester number
MONTH_SEMESTER_NUM = {
    1:1, 2:1, 3:1, 4:1,     # Jan-Apr Winter
    5:2, 6:2,               # May-Jun Spring
    7:3, 8:3,               # Jul-Aug Summer
    9:4, 10:4, 11:4, 12:4,  # Sep-Dec Fall
}

def course_key(course):
    """Return a tuple for sorting courses by year, then semester. """
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


def get_courses(client, all_semesters):
    """Return a list of courses where current user is an admin."""
    user = client.get("/api/users/current/")
    user_pk = user["pk"]
    course_list = client.get(f"/api/users/{user_pk}/courses_is_admin_for/")

    # Remove past courses unless all_semesters is True
    if not all_semesters:
        course_list = filter(is_current_course, course_list)

    # Sort with newest at the top
    course_list = sorted(course_list, key=course_key)
    return course_list


def print_course(course):
    """Print course to stdout."""
    print(
        f"[{course['pk']}] {course['name']} "
        f"{course['semester']} {course['year']}"
    )


def print_dict(obj):
    """Pretty print a dictionary."""
    print(json.dumps(obj, indent=4))


@main.command()
@click.argument("course_pks", nargs=-1)
@click.pass_context
def courses(ctx, course_pks):
    """List courses or show course detail.

    When called with no arguments, list courses.  When called with a course
    primary key, show course detail.

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # If the user doesn't specify a course, list courses
    if not course_pks:
        course_list = get_courses(client, ctx.obj["ALL_SEMESTERS"])
        for i in course_list:
            print_course(i)
        return

    # If the user provides course pks, show course detail
    for course_pk in course_pks:
        course = client.get(f"/api/courses/{course_pk}/")
        print_dict(course)


@main.command()
@click.argument("project_pks", nargs=-1)
@click.pass_context
def projects(ctx, project_pks):
    """List projects or show project detail.

    When called with no arguments, list courses and their projects.  When
    called with a project primary key, show project detail.

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # If the user doesn't specify a project, list courses and projects
    if not project_pks:
        course_list = get_courses(client, ctx.obj["ALL_SEMESTERS"])
        for course in course_list:
            print_course(course)
            project_list = client.get(f"/api/courses/{course['pk']}/projects/")
            project_list = sorted(project_list, key=lambda x: x["name"])
            for project in project_list:
                print(f"  [{project['pk']}] {project['name']}")
        return

    # If the user provides project pks, show project detail
    for project_pk in project_pks:
        project = client.get(f"/api/projects/{project_pk}/")
        print_dict(project)


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


@main.command()
@click.argument("project_pk", nargs=1)
@click.argument("group_pk_or_uniqname", nargs=-1)
@click.pass_context
def groups(ctx, project_pk, group_pk_or_uniqname):
    """List groups or show group detail.

    When called with no arguments, list groups for one project.  When
    called with a group primary key or uniqname, show group detail.
    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # Print course and project
    project = client.get(f"/api/projects/{project_pk}/")
    course = client.get(f"/api/courses/{project['course']}/")
    print(
        f"{course['name']} {course['semester']} {course['year']} "
        f"{project['name']}\n"
    )

    # If the user doesn't specify a group, list groups
    if not group_pk_or_uniqname:
        group_list = client.get(f"/api/projects/{project_pk}/groups/")
        for group in group_list:
            print_group(group)
        return

    # Verify only one group or uniqname
    if len(group_pk_or_uniqname) > 1:
        sys.exit("Error: specify only one group primary key or uniqname")
    group_pk_or_uniqname = group_pk_or_uniqname[0]

    # If the user provides a uniqname, look it up
    if not group_pk_or_uniqname.isnumeric():
        uniqname = group_pk_or_uniqname
        group_list = client.get(f"/api/projects/{project_pk}/groups/")
        matches = filter(lambda x: is_group_member(uniqname, x), group_list)
        matches = list(matches)
        if not matches:
            sys.exit(f"Error: uniqname not in any group: {uniqname}")
        if len(matches) > 1:
            sys.exit(f"Error: uniqname in more than one group: {uniqname}")
        group_pk = matches[0]["pk"]
    else:
        group_pk = group_pk_or_uniqname[0]

    # Show group detail
    group = client.get(f"/api/groups/{group_pk}/")
    print_dict(group)


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
