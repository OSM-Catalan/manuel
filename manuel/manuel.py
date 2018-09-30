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


class Manuel(object):

    def __init__(self, url_config):
        """
        Class constructor
        """

        self.config = ConfigObj(url_config)
        self.conn = psycopg2.connect(**self.config['report']['connection'])

    def create_index(self, url_config, debug=False):
        """
        Creates the index for the queries

        :param url_config: Config file
        :param debug: Enables debug mode
        :type debug: bool
        :return: None
        """

        cur = self.conn.cursor()
        if debug:
            ex_sql = cur.mogrify(self.config['report']['general']['indexs'])
            print(ex_sql)
        cur.execute(self.config['report']['general']['indexs'])
        self.conn.commit()

    def generate_materialized_vies(self, url_config, debug=False):
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

        cur = self.conn.cursor()
        self.config["report"]["general"]["subarea_sql"] = AsIs(self.config["report"]["general"]["subarea_sql"])
        self.config["report"]["general"]["table_name"] = AsIs("manuel_" + self.config["report"]["general"]["table_name"])

        if debug:
            drop_sql = cur.mogrify(sql_drop, self.config['report']['general'])
            print(drop_sql)

        cur.execute(sql_drop, self.config['report']['general'])
        if debug:
            mat_sql = cur.mogrify(sql_create, self.config['report']['general'])
            print(mat_sql)
        cur.execute(sql_create, self.config['report']['general'])
        self.conn.commit()

    def generate_report(self, url_config, debug=False):
        """
        Method to generate the report

        :param url_config: URL to the config file
        :param debug: Enables debug mode
        :type debug: bool
        :return: None
        """

        print('\n')

        base_dir = os.path.join(os.getcwd(), os.path.dirname(url_config))

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        result = {}

        for element in tqdm(self.config['report']['elements'].keys()):
            sql = self.config['report']['elements'][element]['sql']
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
        self.conn.close()

        if not isinstance(self.config['report']['templates'], list):
            templates = [self.config['report']['templates']]
        else:
            templates = self.config['report']['templates']
        for template in templates:
            if debug:
                print("Generating {}".format(template))
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
