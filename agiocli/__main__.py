"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
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
    agio courses eecs485sp21

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # Handle --list: list courses and exit
    if show_list:
        course_list = utils.get_current_course_list(client)
        for i in course_list:
            print(f"[{i['pk']}]\t{i['name']} {i['semester']} {i['year']}")
        return

    # Select a course and print it
    course = utils.get_course_smart(course_arg, client)
    print(utils.dict_str(course))


@main.command()
@click.argument("project_arg", required=False)
@click.option("-c", "--course", "course_arg",
              help="Course pk, name or shorthand.")
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List projects and exit.")
@click.pass_context
def projects(ctx, project_arg, course_arg, show_list):
    """Show project detail or list projects.

    PROJECT_ARG is a primary key, name, or shorthand.

    \b
    EXAMPLES:
    agio projects
    agio projects 1005
    agio projects p1
    agio projects p1 --course 109
    agio projects p1 --course eecs485sp21

    """
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # Handle --list: list projects and exit
    if show_list:
        course = utils.get_course_smart(course_arg, client)
        project_list = utils.get_course_project_list(course, client)
        for i in project_list:
            print(f"[{i['pk']}]\t{i['name']}")
        return

    # Select a project and print it
    project = utils.get_project_smart(project_arg, course_arg, client)
    print(utils.dict_str(project))


@main.command()
@click.argument("group_arg", required=False)
@click.option("-c", "--course", "course_arg",
              help="Course pk, name or shorthand.")
@click.option("-p", "--project", "project_arg",
              help="Project pk, name or shorthand.")
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List groups and exit.")
@click.pass_context
def groups(ctx, group_arg, project_arg, course_arg, show_list):
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])

    # Handle --list: list groups and exit
    if show_list:
        project = utils.get_project_smart(project_arg, course_arg, client)
        group_list = utils.get_group_list(project, client)
        for i in group_list:
            print(utils.group_str(i))
        return

    # Select a group and print it
    project = utils.get_group_smart(group_arg, project_arg, course_arg, client)
    print(utils.dict_str(project))


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
