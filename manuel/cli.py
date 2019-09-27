from __future__ import absolute_import
import click
from manuel.manuel import Manuel


@click.group()
def manuel():
    pass


@manuel.command()
@click.argument('config_file')
@click.option('--index/--no-index', default=False)
@click.option('--recreate/--no-recreate', default=True)
@click.option('--debug/--no-debug', default=False)
@click.option('--name')
def cli_generate_report(config_file, index, recreate, debug, name):
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
    if not name:
        from os.path import basename, splitext
        name = m.config["report"]["general"].get("report_name", None) or \
            splitext(basename(config_file))[0] or 'report'
    result = m.generate_report(config_file, debug, name)
    m.save_results(result, config_file)


def invoke():
    manuel()
