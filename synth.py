#!/usr/bin/env python3
import click
import os
import shutil


@click.command()
@click.option("--name",
              default="my_project",
              help="name of your project")
@click.option("--frontend",
              default="static",
              help="frontend to use")
@click.option("--backend",
              default=None,
              help="backend to use")
@click.option("--database",
              default=None,
              help="database to use")
def synth(name, frontend, backend, database):
    """ creates a synth wireframe with your desired frontend,
    backend, and database
    """
    copy_dir = "/etc/synth/projects_master/nginx_router/"
    allowed_front = ["static", "node", "react"]
    allowed_back = ["node", "flask", "django"]
    allowed_db = ["mysql", "postgres", "mongodb"]

    if not os.path.exists(name):
        os.mkdir(name)
    else:
        raise FileExistsError('Directory {} exists.'.format(name))

    #<---      NGINX ROUTER SECTION     --->#
    #   - handles all container routing -   #
    #   -     thus needed by default    -   #
    os.makedirs("{}/nginx_router/nginx_conf".format(name))

    # NGINX config files
    shutil.copyfile(copy_dir + "nginx_conf/default.conf",
                    "{}/nginx_router/nginx_conf/default.conf"
                    .format(name))
    shutil.copyfile(copy_dir + "nginx_conf/nginx.conf",
                    "{}/nginx_router/nginx_conf/nginx.conf"
                    .format(name))

    # NGINX docker file
    shutil.copyfile(copy_dir + "Dockerfile.dev",
                    "{}/nginx_router/Dockerfile.dev"
                    .format(name))

    #<---        COMPOSE SECTION        --->#
    #   -  base compose file for router -   #
    #   -   gets appended to as needed  -   #
    shutil.copyfile("/etc/synth/projects_master/docker-compose.yml",
                    "{}/docker-compose.yml".format(name))

    #<--- FRONTEND SECTION --->#
    if frontend in allowed_front:

        #<--- STATIC FRONTEND SECTION --->#
        if frontend == "static":
            os.makedirs("{}/nginx_router/frontend/static/styles".format(name))

            # static CSS & HTML content
            shutil.copyfile(copy_dir + "frontend/static/index.html",
                            "{}/nginx_router/frontend/static/index.html"
                            .format(name))
            shutil.copyfile(copy_dir + "frontend/static/styles/common.css",
                            "{}/nginx_router/frontend/static/".format(name) +
                            "styles/common.css")
            shutil.copyfile(copy_dir + "frontend/static/styles/header.css",
                            "{}/nginx_router/frontend/static/".format(name) +
                            "styles/header.css")
            shutil.copyfile(copy_dir + "frontend/static/styles/footer.css",
                            "{}/nginx_router/frontend/static/".format(name) +
                            "styles/footer.css")

        if frontend == "node":
            pass
        if frontend == "react":
            pass


if __name__ == "__main__":
    synth()
