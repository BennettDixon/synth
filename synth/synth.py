#!/usr/bin/env python3
""" CLI portion of synth, a docker bootstrapping tool
    commands:
        - create: creates a docker wireframe with your desired
            frontend, backend, and database
 """

import click
import os
from synth_part_builder import PartBuilder
from synth_part_builder import PartBuilderException
import shutil
import traceback


@click.group()
def cli():
    """ synth is a tool to create and deploy wireframed docker
    images and compose files easily. It was created by Bennett
    Dixon and Jack Gindi."""
    pass


@cli.command()
@click.option("--name",
              "-n",
              default="my_project",
              help="name of your project")
@click.option("--frontend",
              "-f",
              default=None,
              help="frontend to use")
@click.option("--backend",
              "-b",
              default=None,
              help="backend to use")
@click.option("--database",
              "-d",
              default=None,
              help="database to use")
@click.option("--cache",
              "-c",
              default=None,
              help="caching service to use")
@click.option("--pipeline",
              "-p",
              default=None,
              help="ci/cd pipeline to use")
def create(name, frontend, backend, database, cache, pipeline):
    """ creates a synth wireframe with your desired frontend,
    backend, database, caching service, and ci/cd pipeline
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    copy_dir = root_dir + "/projects_master/nginx_router/"

    if not frontend and not backend and not database and not cache:
        click.echo("all synth services can't be None")
        exit(1)

    # make the directory for the project if it doesn't exist
    try:
        os.mkdir(name)
        shutil.copyfile(root_dir + "/projects_master/README.md",
                        "{}/README.md".format(name))
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

    shutil.copyfile(copy_dir + "Dockerfile",
                    "{}/nginx_router/Dockerfile"
                    .format(name))

    #<---        COMPOSE SECTION        --->#
    #   -  base compose file for router -   #
    #   -   gets appended to as needed  -   #
    shutil.copyfile(root_dir +
                    "/projects_master/docker-compose.yml",
                    "{}/docker-compose.yml".format(name))

    # gather some info for the part builder
    front_enabled = False
    if frontend is not None:
        front_enabled = True
    back_enabled = False
    if backend is not None:
        back_enabled = True
    # build PartBuilder instance
    pb = PartBuilder(parts_root=root_dir + "/parts",
                     project_name=name,
                     front_enabled=front_enabled,
                     back_enabled=back_enabled)

    #<--- DATABASE SECTION --->#
    if database is not None:
        if database == "mysql":
            click.echo("MySQL 5.7.6 has permissions issues, " +
                       "using 5.7 instead")
        try:
            # create directory for volume mounting
            os.makedirs("{}/database/data".format(name))

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
            # error out if cache isn't allowed
            click.echo(pbe)
            cleanup(name)

    #<--- FRONTEND SECTION --->#
    if frontend is not None:
        try:
            # copy directory tree into project directory
            shutil.copytree(copy_dir + "frontend/{}"
                            .format(frontend),
                            "{}/nginx_router/frontend/"
                            .format(name))

            # add frontend section to docker-compose file
            pb.add_part(frontend, database, cache)

        except (PartBuilderException, FileNotFoundError) as desc_e:
            # error out if caching service isn't allowed
            if type(desc_e) is FileNotFoundError:
                click.echo("FileNotFoundError: {}".format(desc_e))
            if type(desc_e) is PartBuilderException:
                click.echo("PartBuilderException: {}".format(desc_e))
            cleanup(name)

        except Exception as e:
            # error out if frontend isn't allowed
            traceback.print_tb(e.__traceback__)
            cleanup(name)

    #<--- BACKEND SECTION --->#
    if backend is not None:
        try:
            # copy directory tree into project
            shutil.copytree(copy_dir + "backend/{}"
                            .format(backend),
                            "{}/nginx_router/backend/"
                            .format(name))

            # add backend section to docker-compose file
            pb.add_part(backend, database, cache)

        except (PartBuilderException, FileNotFoundError) as desc_e:
            # error out if caching service isn't allowed
            if type(desc_e) is FileNotFoundError:
                click.echo("FileNotFoundError: {}".format(desc_e))
            if type(desc_e) is PartBuilderException:
                click.echo("PartBuilderException: {}".format(desc_e))
            cleanup(name)

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            cleanup(name)

    #<--- PIPELINE SECTION --->#
    if pipeline is not None:
        try:
            # add and build pipeline yaml file
            pb.build_pipeline(name, pipeline, {
                "frontend": frontend,
                "backend": backend,
                "database": database,
                "cache": cache
            })

        except PartBuilderException as desc_e:
            # error out if pipeline isn't allowed
            click.echo("PartBuilderException: {}".format(desc_e))
            cleanup(name)

    click.echo("\nsynthesized project directory {}".format(name))
    click.echo("run:\n\n\tcd {}; docker-compose up\n"
               .format(name))
    click.echo("to start your development containers!\n")


def cleanup(name):
    """ cleanup operation to remove directory of a failed create """
    shutil.rmtree(name)
    exit(1)


if __name__ == "__main__":
    cli()
