# -*- coding: UTF-8 -*-

import psycopg2
from configobj import ConfigObj
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA
from jinja2 import Template
import os

print '\n'


config = ConfigObj('report.conf')

conn = psycopg2.connect(**config['report']['connection'])
cur = conn.cursor()
cur.execute(config['report']['general']['subarea_sql'], config['report']['general'])
data = cur.fetchall()

result = []
widgets = [Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()]

pbar = ProgressBar(widgets=widgets, maxval=len(data)).start()
for index, poblacio in enumerate(data):
    pbar.update(index+1)
    element_vars = {}
    for element in config['report']['elements'].keys():
        sql = config['report']['elements'][element]['sql']
        cur.execute(sql, (str(poblacio[0]),))
        element_vars[element] = cur.fetchall()[0]

    element_vars['id'] = int(abs(poblacio[0]))
    element_vars['name'] = poblacio[1]
    result.append(element_vars)

conn.close()

if not isinstance(config['report']['templates'], list):
    templates = [config['report']['templates']]
else:
    templates = config['report']['templates']
for template in templates:
    f = open(template)
    base, extension = os.path.splitext(template)
    temp = f.read()
    f.close()
    t = Template(temp)

    report_data = t.render(data=result)
    f = open('report'+str(extension), 'w')
    f.write(report_data)
    f.close()
print '\nDone\n'
