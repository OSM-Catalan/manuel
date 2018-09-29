# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor
from configobj import ConfigObj

from tqdm import tqdm
from jinja2 import Template
import os
import sys


def create_index(url_config, debug=False):
    """
    Creates the index for the queries

    :param url_config: Config file
    :param debug: Enables debug mode
    :type debug: bool
    :return: None
        """

    config = ConfigObj(url_config)
    conn = psycopg2.connect(**config['report']['connection'])
    cur = conn.cursor()
    if debug:
        ex_sql = cur.mogrify(config['report']['general']['indexs'])
        print(ex_sql)
    cur.execute(config['report']['general']['indexs'])
    conn.commit()


def generate_materialized_vies(url_config, debug=False):
    """
    Generates the materialized vies

    :param url_config: URL of the configuration file
    :param debug: Debug mode:
    :type debug: bool
    :return: None
    :rtype: None
    """

    sql_create = """
    CREATE MATERIALIZED VIEW %(table_name)s as (%(subarea_sql)s);
    """
    sql_drop = """
    DROP MATERIALIZED VIEW IF EXISTS %(table_name)s;
    """
    config = ConfigObj(url_config)

    conn = psycopg2.connect(**config['report']['connection'])
    cur = conn.cursor()
    config["report"]["general"]["subarea_sql"] = AsIs(config["report"]["general"]["subarea_sql"])
    config["report"]["general"]["table_name"] = AsIs("manuel_" + config["report"]["general"]["table_name"])

    if debug:
        drop_sql = cur.mogrify(sql_drop, config['report']['general'])
        print(drop_sql)

    cur.execute(sql_drop, config['report']['general'])
    if debug:
        mat_sql = cur.mogrify(sql_create, config['report']['general'])
        print(mat_sql)
    cur.execute(sql_create, config['report']['general'])
    conn.commit()


def generate_report(url_config, debug=False):
    """
    Method to generate the report

    :param url_config: URL to the config file
    :param debug: Enables debug mode
    :type debug: bool
    :return: None
    """

    print('\n')

    config = ConfigObj(url_config)
    base_dir = os.path.join(os.getcwd(), os.path.dirname(url_config))

    conn = psycopg2.connect(**config['report']['connection'])
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    result = {}

    for element in tqdm(config['report']['elements'].keys()):
        sql = config['report']['elements'][element]['sql']
        if debug:
            ex_sql = cur.mogrify(sql)
            print(ex_sql)
        cur.execute(sql)
        element_vars = cur.fetchall()
        for e in element_vars:
            dict_element = dict(e)
            name = dict_element["subarea_name"]
            if name not in result:
                result[name] = {}
            result[name].update(dict_element)
    conn.close()

    if not isinstance(config['report']['templates'], list):
        templates = [config['report']['templates']]
    else:
        templates = config['report']['templates']
    for template in templates:
        url_template = os.path.join(base_dir, template)
        f = open(url_template)
        base, extension = os.path.splitext(url_template)
        temp = f.read()
        f.close()
        t = Template(temp)

        report_data = t.render(data=result)
        url_out = os.path.join(base_dir, 'report'+str(extension))
        f = open(url_out, 'w')
        f.write(report_data)
        f.close()
    print ('\nDone\n')


if __name__ == "__main__":
    generate_report(sys.argv[1])
