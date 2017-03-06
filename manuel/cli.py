from __future__ import absolute_import
import click
from manuel.manuel import generate_report
from manuel.manuel import create_index


@click.group()
def manuel():
    pass


def invoke():
    manuel()


@manuel.command()
@click.argument('config_file')
@click.option('--index/--no-index', default=False)
def cli_generate_report(config_file, index):
    if index:
        create_index(config_file)
    generate_report(config_file)
