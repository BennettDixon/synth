#!/usr/bin/env python3
import click
import os
import shutil

@click.group()
def cli():
    pass

@cli.command()
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
def create(name, frontend, backend, database):
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
        click.echo('Frontend {} not allowed: synth --help for more info'
                   .format(frontend))
        exit(1)

    #<--- BACKEND SECTION --->#
    if backend in allowed_back:

        #<--- FLASK BACKEND SECTION --->#
        if backend == "flask":
            shutil.copytree(copy_dir + "backend/flask/",
                            "{}/nginx_router/backend/flask/".format(name))

        elif backend == "node":
            click.echo('feature not implemented . . . yet!')

        elif backend == "django":
            click.echo('feature not implemented . . . yet!')

        else:
            # error out if backend isn't allowed
            click.echo('Backend {} is not allowed: synth --help for more info'
                       .format(backend))
            exit(1)

    #<--- DATABASE SECTION --->#
    if database in allowed_db:

        #<--- --->#
        if database == "mysql":
            click.echo('feature not implemented . . . yet!')
        
        elif backend == "mongo":
            click.echo('feature not implemented . . . yet!')

        elif backend == "postgres":
            click.echo('feature not implemented . . . yet!')

        else:
            # error out if backend isn't allowed
            click.echo('Database {} is not allowed: synth --help for more info'
                       .format(database))
            exit(1)
        
if __name__ == "__main__":
    cli()
