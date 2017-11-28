# -*- coding: utf-8 -*-
import unittest
import re
from jinja2 import Template
from lxml import etree


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.result = [
            dict(
                id='001',
                name='name1',
                len_residential_noname = [1000.123, 10.123],
                len_livingstreet_noname = [1001.123, 10.99],
                len_residential_total = [1002.123, 12.123],
                len_livingstreet_total = [1003.123, 13.123]
            ),
            dict(
                id='002',
                name='name2',
                len_residential_noname = [2000, 20],
                len_livingstreet_noname = [2001, 21],
                len_residential_total = [2002, 22],
                len_livingstreet_total = [2003, 23]
            ),
        ]
        
    def render(self, url_template):
        with open(url_template) as f:
            temp = f.read()
        t = Template(temp)
        return t.render(data=self.result)

    def get_expected(self, record):
        expected = [
            record['id'],
            record['name'],
            '{:.0f}'.format(record['len_residential_noname'][0]),
            '{:.0f}'.format(record['len_residential_noname'][1]),
            '{:.0f}'.format(record['len_livingstreet_noname'][0]),
            '{:.0f}'.format(record['len_livingstreet_noname'][1]),
            '{:.0f}'.format(record['len_residential_noname'][0] \
                + record['len_livingstreet_noname'][0]),
            '{:.0f}'.format(record['len_residential_total'][0] \
                + record['len_livingstreet_total'][0]),
            '{:.1f}%'.format(record['len_residential_total'][0] \
                + record['len_livingstreet_total'][0] and \
                ((record['len_residential_noname'][0] \
                + record['len_livingstreet_noname'][0]) \
                / (record['len_residential_total'][0] \
                + record['len_livingstreet_total'][0])) * 100)
        ]
        return expected


class TestTowns(BaseTest):

    def test_csv(self):
        url_template = 'towns/template.csv'
        report_data = self.render(url_template)
        for row, record in zip(report_data.split('\n'), self.result):
            expected = ';'.join(self.get_expected(record)[1:-1])
            self.assertEqual(row, expected)

    def test_wiki(self):
        url_template = 'towns/template.wiki'
        report_data = self.render(url_template)
        self.assertEqual(report_data[:2], '{|')
        self.assertEqual(report_data[-3:], '|}\n')
        self.assertEqual(report_data.count('!'), 10)
        self.assertEqual(report_data.count('|-'), 3)
        report_data = report_data[report_data.find('|-')+2:-3]
        for row, record in zip(report_data.split('|-'), self.result):
            expected = self.get_expected(record)
            for field, exp_val in zip(row.split('\n')[1:-1], expected):
                value = field.split('| ')[-1]
                self.assertEqual(value, exp_val)

    def test_html(self):
        url_template = 'towns/template.html'
        report_data = self.render(url_template)
        root = etree.fromstring(report_data)
        for row, record in zip(root.findall('body/table/tbody/tr'), self.result):
            expected = self.get_expected(record)
            for field, exp_val in zip(row.findall('td')[:-1], expected):
                self.assertEqual(field.text, exp_val)

