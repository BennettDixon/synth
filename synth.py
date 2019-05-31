#!/usr/bin/env python3
import click

@click.command()
@click.option("--frontend",
              default="static",
              help="frontend to use")
@click.option("--backend",
              default=None,
              help="backend to use")
@click.option("--database",
              default=None,
              help="database to use")
def synth(frontend, backend, database):
    """ creates a synth wireframe with your desired frontend,
    backend, and database
    """
    print(frontend)
    print('hi')
