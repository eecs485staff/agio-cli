"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import json
import click
from agiocli import APIClient


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
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
def users(ctx):
    """List current user."""
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

    # If the user doesn't specify a course, the list them
    if not course_pks:
        user = client.get("/api/users/current/")
        user_pk = user["pk"]
        course_list = client.get(f"/api/users/{user_pk}/courses_is_admin_for/")
        course_list = sorted(course_list, key=lambda x: x["pk"], reverse=True)
        for i in course_list:
            print(f"[{i['pk']}] {i['name']} {i['semester']} {i['year']}")
        return

    # If the user provides course pks, show detail on course and projects
    for course_pk in course_pks:
        course = client.get(f"/api/courses/{course_pk}/")
        print(
            f"[{course['pk']}] {course['name']} "
            f"{course['semester']} {course['year']}"
        )
        project_list = client.get(f"/api/courses/{course['pk']}/projects/")
        project_list = sorted(project_list, key=lambda x: x["name"])
        for i in project_list:
            print(f"  [{i['pk']}] {i['name']}")


@main.command()
@click.argument("project_pk", nargs=1)
@click.pass_context
def projects(ctx, project_pk):
    """List projects or show project detail.

    When called with no arguments, list courses and their projects.  When
    called with a project primary key, show project detail.

    """
    # FIXME list courses with nested projects here
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    project = client.get(f"/api/projects/{project_pk}/")
    print(json.dumps(project, indent=4))


@main.command()
@click.argument("project_pk", nargs=1)
@click.pass_context
def groups(ctx, project_pk):
    """List groups or show group detail."""
    client = APIClient.make_default(debug=ctx.obj["DEBUG"])
    project = client.get(f"/api/projects/{project_pk}/")
    course = client.get(f"/api/courses/{project['course']}/")
    # FIXME copied code for printing a course
    print(
        f"{course['name']} {course['semester']} "
        f"{course['year']} {project['name']}"
    )
    group_list = client.get(f"/api/projects/{project_pk}/groups/")
    # FIXME pretty-print groups
    print(json.dumps(group_list, indent=4))
    # FIXME handle group detail pk


if __name__ == "__main__":
    # These errors are endemic to click
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    main(obj={})
