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
def create(name, frontend, backend, database):
    """ creates a synth wireframe with your desired frontend,
    backend, and database
    """
    copy_dir = "/etc/synth/projects_master/nginx_router/"
    allowed_front = PartBuilder.allowed_frontends
    allowed_back = PartBuilder.allowed_backends
    allowed_db = PartBuilder.allowed_databases    

    if not frontend and not backend and not database:
        click.echo("all synth services can't be None")
        exit(1)
    
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

    pb = PartBuilder(parts_root="/etc/synth/parts",
                     nginx_file="{}/nginx_router/nginx_conf/default.conf"
                     .format(name),
                     compose_file="{}/docker-compose.yml")
    
    #<--- FRONTEND SECTION --->#
    if frontend is not None:
        if frontend in allowed_front:

            if frontend == "static":
                shutil.copytree(copy_dir + "frontend/static/",
                                "{}/nginx_router/frontend/static/"
                                .format(name))
                
            elif frontend == "node":
                shutil.copytree(copy_dir + "frontend/node/",
                                "{}/nginx_router/frontend/node/"
                                .format(name))
                
            elif frontend == "react":
                click.echo('feature not implemented . . . yet!')
    
            else:
                # error out if frontend isn't allowed
                raise PartBuilderException("frontend {} is not allowed"
                                           .format(frontend))

            # add frontend section to docker-compose file
            pb.add_part(frontend)

    #<--- BACKEND SECTION --->#
    if backend is not None:
        if backend in allowed_back:

            if backend == "flask":
                shutil.copytree(copy_dir + "backend/flask/",
                                "{}/nginx_router/backend/flask/".format(name))

            elif backend == "node":
                click.echo('feature not implemented . . . yet!')

            elif backend == "django":
                click.echo('feature not implemented . . . yet!')
                    
            else:
                # error out if backend isn't allowed
                raise PartBuilderException("backend {} is not allowed"
                                           .format(backend))

            # add backend section to docker-compose file
            pb.add_part(backend)

    #<--- DATABASE SECTION --->#
    if database is not None:
        if database in allowed_db:

            if database == "mysql":
                click.echo('feature not implemented . . . yet!')
        
            elif database == "mongo":
                click.echo('feature not implemented . . . yet!')

            elif database == "postgres":
                click.echo('feature not implemented . . . yet!')

            else:
                # error out if backend isn't allowed
                raise PartBuilderException("database {} is not allowed"
                                           .format(database))

            # add database section to docker-compose file
            pb.add_part(database)

if __name__ == "__main__":
    cli()
