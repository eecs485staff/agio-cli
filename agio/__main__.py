"""
A command line interface to autograder.io.

Andrew DeOrio <awdeorio@umich.edu>
"""
import json
import click
import agcli


# FIXME global variable
# https://click-docs-cn.readthedocs.io/zh_CN/latest/commands.html#nested-handling-and-contexts
DEBUG = False


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-d", "--debug", is_flag=True, help="Debug output")
def main(debug):
    """Autograder.io command line interface."""
    global DEBUG
    DEBUG = debug


@main.command()
def users():
    client = agcli.APIClient.make_default(debug=DEBUG)
    user = client.get("/api/users/current/")
    print(json.dumps(user, indent=4))
    # print(f"{user['username']} {user['first_name']} {user['last_name']}")


@main.command()
@click.argument("course_pks", nargs=-1)
def courses(course_pks):
    """List courses (no args) or show course detail."""
    client = agcli.APIClient.make_default(debug=DEBUG)

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
        print(f"[{course['pk']}] {course['name']} {course['semester']} {course['year']}")
        project_list = client.get(f"/api/courses/{course['pk']}/projects/")
        project_list = sorted(project_list, key=lambda x: x["name"])
        for i in project_list:
            print(f"  [{i['pk']}] {i['name']}")


@main.command()
@click.argument("project_pk", nargs=1)
def projects(project_pk):
    client = agcli.APIClient.make_default(debug=DEBUG)
    project = client.get(f"/api/projects/{project_pk}/")
    print(json.dumps(project, indent=4))


@main.command()
@click.argument("project_pk", nargs=1)
def groups(project_pk):
    client = agcli.APIClient.make_default(debug=DEBUG)
    project = client.get(f"/api/projects/{project_pk}/")
    course = client.get(f"/api/courses/{project['course']}/")
    print(f"{course['name']} {course['semester']} {course['year']} {project['name']}")
    group_list = client.get(f"/api/projects/{project_pk}/groups/")
    # FIXME pretty-print groups
    print(json.dumps(group_list, indent=4))



if __name__ == "__main__":
    # This error is endemic to click
    # pylint: disable=no-value-for-parameter
    main()
