#!/usr/bin/env python3
""" CLI portion of synth, a docker bootstrapping tool
    commands:
        - create: creates a docker wireframe with your desired
            frontend, backend, and database
 """

import click
import os
import shutil
from part_builder import PartBuilder
from part_builder import PartBuilderException


@click.group()
def cli():
    """ group class to allow expandability """
    pass


@cli.command()
@click.option("--name",
              default="my_project",
              help="name of your project")
@click.option("--frontend",
              default=None,
              help="frontend to use")
@click.option("--backend",
              default=None,
              help="backend to use")
@click.option("--database",
              default=None,
              help="database to use")
@click.option("--cache",
              default=None,
              help="caching service to use")
def create(name, frontend, backend, database, cache):
    """ creates a synth wireframe with your desired frontend,
    backend, and database
    """
    copy_dir = "/etc/synth/projects_master/nginx_router/"

    if not frontend and not backend and not database and not cache:
        click.echo("all synth services can't be None")
        exit(1)

    # checks for node, which can be used for both FE and BE
    if frontend == "node":
        frontend = "node_front"

    if backend == "node":
        backend = "node_back"

    # make the directory for the project if it doesn't exist
    try:
        os.mkdir(name)
    except FileExistsError:
        click.echo('Directory {} already exists.'
                   .format(name) +
                   " Please choose a different name.")
        exit(1)

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

    # build PartBuilder instance
    pb = PartBuilder(parts_root="/etc/synth/parts",
                     nginx_file="{}/nginx_router/nginx_conf/default.conf"
                     .format(name),
                     compose_file="{}/docker-compose.yml"
                     .format(name))

    #<--- DATABASE SECTION --->#
    if database is not None:
        try:
            # add database section to docker-compose file
            pb.add_part(database)

        except PartBuilderException as pbe:
            # error out if the database isn't allowed
            click.echo(pbe)
            cleanup(name)

    #<--- CACHING SECTION --->#
    if cache is not None:
        try:
            # add cache section to docker-compose file
            pb.add_part(cache)

        except PartBuilderException as pbe:
            # error out if caching service isn't allowed
            click.echo(pbe)
            cleanup(name)

    #<--- FRONTEND SECTION --->#
    if frontend is not None:
        try:
            # copy directory tree into project directory
            shutil.copytree(copy_dir + "/frontend/{}"
                            .format(frontend),
                            "{}/projects_master/nginx_router/frontend"
                            .format(name))

            # add frontend section to docker-compose file
            pb.add_part(frontend)

        except PartBuilderException as pbe:
            # error out if frontend isn't allowed
            click.echo(pbe)
            cleanup(name)

    #<--- BACKEND SECTION --->#
    if backend is not None:
        try:
            # copy directory tree into project
            shutil.copytree(copy_dir + "/backend/{}"
                            .format(backend),
                            "{}/projects_master/nginx_router/backend"
                            .format(name))

            # add backend section to docker-compose file
            pb.add_part(backend, database, cache)

        except PartBuilderException as pbe:
                # error out if backend isn't allowed
                click.echo(pbe)
                cleanup(name)

    click.echo("\nsynthesized project directory {}".format(name))
    click.echo("run:\n\n\tcd {}; docker-compose up --build\n"
               .format(name))
    click.echo("to start your development containers!\n")


@cli.command()
@click.option("--pods",
              default=1,
              help="number of frontend pods to use")
def deploy(pods):
    """ deploy your synth project on the current server """
    click.echo(pods)

def cleanup(name):
    """ cleanup operation to remove directory of a failed create """
    shutil.rmtree(name)
    exit(1)

if __name__ == "__main__":
    cli()
