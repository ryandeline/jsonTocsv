#!/usr/bin/env python
#
# Reads an array of JSON objects and writes out CSV-format,
# with key names in first row.
# Columns will be union of all keys in the objects.
#

import csv
import json
import sys

import __init__ as parse

try:
    import settings_local
except ImportError:
    raise ImportError('You must create a settings_local.py file with an ' +
                      'APPLICATION_ID, REST_API_KEY, and a MASTER_KEY ' +
                      'to run tests.')

parse.APPLICATION_ID = settings_local.APPLICATION_ID
parse.REST_API_KEY = settings_local.REST_API_KEY

for parseObject in settings_local.PARSE_CLASSES:
    query = parse.ObjectQuery(parseObject)
    limit = 100
    skip = 0
    counter = 0

    query = query.limit(limit).skip(skip)
    results = query.fetch()

    columns = set()
    for item in results:
        columns.update(set(item))

    with open(parseObject+'.csv', 'w', newline='') as fo:
        #write header
        writer = csv.writer(fo)
        writer.writerow(list(columns))
        #write body using limit & skip to get all records in parse
        while 1:
            for item in results:
                counter += 1
                row = []
                for c in columns:
                    if c in item: row.append(str(item[c]))
                    else: row.append('')
                writer.writerow(row)

            if counter == 0:
                break
            else:
                counter = 0
                skip = skip + limit
                query = query.limit(limit).skip(skip)
                results = query.fetch()
