import logging
import sys
from os import getenv
import click
from icecream import ic
from microservice.core import Core


@click.group()
def cli():
    """General command line interface."""


@cli.group(help='Webserver commands')
def web():
    pass


@cli.group(help='Miscellaneous commands')
def misc():
    pass


@cli.group(help='Database commands')
def db():
    pass


@web.command(help='Run web dev server')
def run():
    conf_file = getenv('MS_CONFIG')
    if conf_file is None:
        ic()
        click.echo(
            click.style(
                'MS_CONFIG variable is not defined',
                fg='red',
                bold=True
            )
        )
        sys.exit(1)
    core_obj = Core()
    core_obj.config.from_yaml(conf_file)
    core_obj.init_resources()
    logging.info('logging initialized')
    web_app = core_obj.web_app()
    web_app.run()


if __name__ == '__main__':
    cli()
