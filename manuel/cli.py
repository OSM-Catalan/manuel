from __future__ import absolute_import
import click
from manuel.manuel import Manuel


@click.group()
def manuel():
    pass


@manuel.command()
@click.argument('config_file')
@click.option('--index/--no-index', default=False)
@click.option('--recreate/--no-recreate', default=False)
@click.option('--debug/--no-debug', default=False)
def cli_generate_report(config_file, index, recreate, debug):
    """
    CLI entry point

    :param config_file:
    :param index:
    :param recreate: Recreates the materialized view
    :type recreate: bool
    :param debug:Enables debug mode
    :type debug: bool
    :return:
    """
    m = Manuel(config_file)
    if index:
        m.create_index(config_file, debug)
    if recreate:
        m.generate_materialized_vies(config_file, debug)
    result = m.generate_report(config_file, debug)
    m.save_results(result, config_file)


def invoke():
    manuel()
