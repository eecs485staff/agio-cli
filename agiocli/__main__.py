"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import sys
import click
from agiocli import APIClient, utils


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
    ctx.obj["ALL"] = all_semesters


@main.command()
@click.pass_context
def login(ctx):
    """Show current authenticated user."""
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    user = client.get("/api/users/current/")
    print(f"{user['username']} {user['first_name']} {user['last_name']}")


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
        user = client.get("/api/users/current/")
        user_pk = user["pk"]
        course_list = client.get(f"/api/users/{user_pk}/courses_is_admin_for/")
        course_list = utils.filter_courses(course_list, ctx.obj["ALL"])
        for i in course_list:
            utils.print_course(i)
        return

    # If the user provides course pks, show course detail
    for course_pk in course_pks:
        course = client.get(f"/api/courses/{course_pk}/")
        utils.print_dict(course)


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
        user = client.get("/api/users/current/")
        user_pk = user["pk"]
        course_list = client.get(f"/api/users/{user_pk}/courses_is_admin_for/")
        course_list = utils.filter_courses(course_list, ctx.obj["ALL"])
        for course in course_list:
            utils.print_course(course)
            project_list = client.get(f"/api/courses/{course['pk']}/projects/")
            project_list = sorted(project_list, key=lambda x: x["name"])
            for project in project_list:
                print(f"  [{project['pk']}] {project['name']}")
        return

    # If the user provides project pks, show project detail
    for project_pk in project_pks:
        project = client.get(f"/api/projects/{project_pk}/")
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
        matches = filter(
            lambda x: utils.is_group_member(uniqname, x),
            group_list
        )
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
    utils.print_dict(group)


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
