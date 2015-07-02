#!/usr/bin/env python
#
# Reads an array of JSON objects and writes out CSV-format,
# with key names in first row.
# Columns will be union of all keys in the objects.
#

import csv
import json
import sys

#import __init__ as parse_rest

with open('Sensor.json') as fi:
    data = json.load(fi)

json_array = data['results']

columns = set()
for item in json_array:
    columns.update(set(item))


with open('Sensor.csv', 'w', newline='') as fo:
    writer = csv.writer(fo)

    writer.writerow(list(columns))
    for item in json_array:
        row = []
        for c in columns:
            if c in item: row.append(str(item[c]))
            else: row.append('')
        writer.writerow(row)
