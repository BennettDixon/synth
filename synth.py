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
    allowed_front = ["static", "node", "react"]
    allowed_back = ["node", "flask", "django"]
    allowed_db = ["mysql", "postgres", "mongodb"]

    if not os.path.exists(name):
        os.mkdir(name)
    else:
        raise FileExistsError('Directory {} exists.'.format(name))
    
    if frontend == "static":
        os.mkdirs("{}/nginx_router/frontend/static".format(name))
        os.mkdir("{}/nginx_router/nginx_conf")
        shutil.copyfile("/usr/bin/synth/master/index.html",
                        "{}/nginx_router/frontend/static/index.html"
                        .format(name))
    print(frontend)
    print('hi')
    
