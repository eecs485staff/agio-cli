"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import sys
import click
from agiocli import APIClient, TokenFileNotFound, utils


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
@click.option("-d", "--debug", is_flag=True, help="Debug output")
@click.pass_context
def main(ctx, debug):
    """Autograder.io command line interface."""
    # Pass global flags to subcommands via Click context
    # https://click.palletsprojects.com/en/latest/commands/#nested-handling-and-contexts
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@main.command()
@click.pass_context
def login(ctx):
    """Show current authenticated user."""
    try:
        client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    except TokenFileNotFound as err:
        sys.exit(err)
    user = client.get("/api/users/current/")
    print(f"{user['username']} {user['first_name']} {user['last_name']}")


@main.command()
@click.argument("course_arg", required=False)
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List courses and exit.")
@click.option("-w", "--web", is_flag=True, help="Open course in browser.")
@click.pass_context
# The \b character in the docstring prevents Click from rewraping a paragraph.
# We need to tell pycodestyle to ignore it.
# https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping
def courses(ctx, course_arg, show_list, web):  # noqa: D301
    """Show course detail or list courses.

    COURSE_ARG is a primary key, name, or shorthand.

    \b
    EXAMPLES:
    agio courses --list
    agio courses
    agio courses 109
    agio courses eecs485sp21

    """
    try:
        client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    except TokenFileNotFound as err:
        sys.exit(err)

    # Handle --list: list courses and exit
    if show_list:
        course_list = utils.get_current_course_list(client)
        for i in course_list:
            print(utils.course_str(i))
        return

    # Select a course and print or open it
    course = utils.get_course_smart(course_arg, client)
    if web:
        utils.open_web(f"https://autograder.io/web/course/{course['pk']}")
        return
    print(utils.dict_str(course))


@main.command()
@click.argument("project_arg", required=False)
@click.option("-c", "--course", "course_arg",
              help="Course pk, name, or shorthand.")
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List projects and exit.")
@click.option("-w", "--web", is_flag=True, help="Open project in browser.")
@click.pass_context
# The \b character in the docstring prevents Click from rewraping a paragraph.
# We need to tell pycodestyle to ignore it.
# https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping
def projects(ctx, project_arg, course_arg, show_list, web):  # noqa: D301
    """Show project detail or list projects.

    PROJECT_ARG is a primary key, name, or shorthand.

    \b
    EXAMPLES:
    agio projects --list
    agio projects
    agio projects 1005
    agio projects --course 109 p1
    agio projects --course eecs485sp21 p1
    agio projects p1

    """
    try:
        client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    except TokenFileNotFound as err:
        sys.exit(err)

    # Handle --list: list projects and exit
    if show_list:
        course = utils.get_course_smart(course_arg, client)
        project_list = utils.get_course_project_list(course, client)
        for i in project_list:
            print(utils.project_str(i))
        return

    # Select a project and print or open it
    project = utils.get_project_smart(project_arg, course_arg, client)
    if web:
        utils.open_web(f"https://autograder.io/web/project/{project['pk']}")
        return
    print(utils.dict_str(project))


@main.command()
@click.argument("group_arg", required=False)
@click.option("-c", "--course", "course_arg",
              help="Course pk, name, or shorthand.")
@click.option("-p", "--project", "project_arg",
              help="Project pk, name, or shorthand.")
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List groups and exit.")
@click.option("-w", "--web", is_flag=True, help="Open group in browser.")
@click.pass_context
# The \b character in the docstring prevents Click from rewraping a paragraph.
# We need to tell pycodestyle to ignore it.
# https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping
def groups(ctx, group_arg, project_arg, course_arg, show_list, web):  # noqa: D301
    """Show group detail or list groups.

    GROUP_ARG is a primary key, name, or member uniqname.

    \b
    EXAMPLES:
    agio groups --list
    agio groups
    agio groups 246965
    agio groups awdeorio
    agio groups awdeorio --project 1005
    agio groups awdeorio --course eecs485sp21 --project p1

    """
    # We must have an function argument for each CLI argument or option
    # pylint: disable=too-many-arguments

    try:
        client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    except TokenFileNotFound as err:
        sys.exit(err)

    # Handle --list: list groups and exit
    if show_list:
        project = utils.get_project_smart(project_arg, course_arg, client)
        group_list = utils.get_group_list(project, client)
        for i in group_list:
            print(utils.group_str(i))
        return

    # Select a group and print or open it
    group = utils.get_group_smart(group_arg, project_arg, course_arg, client)
    if web:
        utils.open_web(
            "https://autograder.io/web/"
            f"project/{group['project']}"
            f"?current_tab=student_lookup"
            f"&current_student_lookup={group['pk']}"
        )
        return
    print(utils.dict_str(group))


@main.command()
@click.argument("submission_arg", required=False)
@click.option("-c", "--course", "course_arg",
              help="Course pk, name, or shorthand.")
@click.option("-p", "--project", "project_arg",
              help="Project pk, name, or shorthand.")
@click.option("-g", "--group", "group_arg",
              help="Group pk or member uniqname.")
@click.option("-l", "--list", "show_list", is_flag=True,
              help="List groups and exit.")
@click.option("-d", "--download", is_flag=True,
              help="Download submission files.")
@click.pass_context
# The \b character in the docstring prevents Click from rewraping a paragraph.
# We need to tell pycodestyle to ignore it.
# https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping
def submissions(ctx, submission_arg, group_arg,
                project_arg, course_arg, show_list, download):  # noqa: D301
    """Show submission detail or list submissions.

    SUBMISSION_ARG is a primary key, 'best', or 'last'

    \b
    EXAMPLES:
    agio submissions --list
    agio submissions
    agio submissions 1128572
    agio submissions --course eecs485sp21 --project p1 --group awdeorio
    agio submissions [...] best
    agio submissions [...] last
    agio submissions [...] --download
    """
    # We must have an function argument for each CLI argument or option
    # pylint: disable=too-many-arguments

    try:
        client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    except TokenFileNotFound as err:
        sys.exit(err)

    # Handle --list: list submissions and exit
    if show_list:
        group = utils.get_group_smart(
            group_arg, project_arg, course_arg, client
        )
        submission_list = utils.get_submission_list(group, client)
        for i in submission_list:
            print(utils.submission_str(i))
        return

    # Select a submission
    submission = utils.get_submission_smart(
        submission_arg, group_arg, project_arg, course_arg, client
    )

    # Handle --download: download the submission and exit
    if download:
        utils.download_submission(submission, group_arg, client)
        return

    # Default: print submission
    print(utils.dict_str(submission))


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
