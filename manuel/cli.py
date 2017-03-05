from __future__ import absolute_import
import click
from manuel.manuel import generate_report


@click.group()
def manuel():
    pass


def invoke():
    manuel()


@manuel.command()
@click.argument('config_file')
def cli_generate_report(config_file):
    generate_report(config_file)
