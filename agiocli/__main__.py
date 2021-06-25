"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import sys
import click
from agiocli import APIClient, utils


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
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
    ctx.obj["ALL"] = all_semesters


@main.command()
@click.pass_context
def login(ctx):
    """Show current authenticated user."""
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    user = client.get("/api/users/current/")
    print(f"{user['username']} {user['first_name']} {user['last_name']}")


@main.command()
@click.argument("course_arg", required=False)
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List courses and exit.")
@click.pass_context
# The \b character in the docstring prevents Click from rewraping a paragraph.
# We need to tell pycodestyle to ignore it.
# https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping
def courses(ctx, course_arg, show_list):  # noqa: D301
    """Show course detail or list courses.

    COURSE_ARG is a primary key, name, or shorthand.

    \b
    EXAMPLES:
    agio courses
    agio courses 109
    agio courses "EECS 485 Spring 2021"
    agio courses eecs485sp21

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # User provides course PK
    if course_arg and course_arg.isnumeric():
        course = client.get(f"/api/courses/{course_arg}/")
        utils.print_dict(course)
        return

    # Get a list of courses sorted by year, semester and name
    user = client.get("/api/users/current/")
    course_list = client.get(f"/api/users/{user['pk']}/courses_is_admin_for/")
    course_list = sorted(course_list, key=utils.course_key, reverse=True)

    # Handle --list: list courses and exit
    if show_list:
        for i in course_list:
            print(f"[{i['pk']}]\t{i['name']} {i['semester']} {i['year']}")
        return

    # FIXME comment
    course = utils.smart_course_select(course_arg, course_list)

    # Show course detail
    utils.print_dict(course)


@main.command()
@click.argument("project_arg", required=False)
@click.option("-c", "--course", "course_arg", help="Debug output")
@click.pass_context
def projects(ctx, project_arg, course_arg):
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # User provides project PK
    if project_arg and project_arg.isnumeric():
        project = client.get(f"/api/projects/{project_arg}/")
        utils.print_dict(project)
        return

    # Select a course
    user = client.get("/api/users/current/")
    course_list = client.get(f"/api/users/{user['pk']}/courses_is_admin_for/")
    course_list = sorted(course_list, key=utils.course_key, reverse=True)
    course = utils.smart_course_select(course_arg, course_list)

    # Get a list of projects for this course, sorted by name
    project_list = client.get(f"/api/courses/{course['pk']}/projects/")
    project_list = sorted(project_list, key=lambda x: x["name"])
    if not project_list:
        # FIXME better error message
        sys.exit("Error: No projects for course, try 'agio courses -l'")

    # FIXME comment
    project = utils.smart_project_select(project_arg, project_list)

    # Show project detail
    utils.print_dict(project)


@main.command()
@click.argument("project_pk", nargs=1)
@click.argument("group_pk_or_uniqname", nargs=-1)
@click.pass_context
def groups(ctx, project_pk, group_pk_or_uniqname):
    """List groups or show group detail.

    When called without a group primary key or uniquename, list groups for one
    project.  When called with a group primary key or uniqname, show group
    detail.

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # Print course and project
    project = client.get(f"/api/projects/{project_pk}/")
    course_pk = project['course']
    course = client.get(f"/api/courses/{course_pk}/")
    print(
        f"{course['name']} {course['semester']} {course['year']} "
        f"{project['name']}\n"
    )

    # If the user doesn't specify a group, list groups
    if not group_pk_or_uniqname:
        group_list = client.get(f"/api/projects/{project_pk}/groups/")
        for group in group_list:
            utils.print_group(group)
        return

    # Verify only one group or uniqname
    if len(group_pk_or_uniqname) > 1:
        sys.exit("Error: specify only one group primary key or uniqname")
    group_pk_or_uniqname = group_pk_or_uniqname[0]

    # If the user provides a uniqname, look it up
    if not group_pk_or_uniqname.isnumeric():
        uniqname = group_pk_or_uniqname
        group_list = client.get(f"/api/projects/{project_pk}/groups/")
        group = utils.find_group(uniqname, group_list)
        group_pk = group["pk"]
    else:
        group_pk = group_pk_or_uniqname[0]

    # Show group detail
    group = client.get(f"/api/groups/{group_pk}/")
    utils.print_dict(group)


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
