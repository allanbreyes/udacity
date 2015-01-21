#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
from pymongo import MongoClient
import json

JSONFILE = 'data/austin-subset.osm.json'

client = MongoClient('mongodb://localhost:27017/')
db = client.austinsubset
collection = db.test

with open(JSONFILE, 'r') as f:
    for line in f.read().split('\n'):
        if line:
            try:
                json_line = json.loads(line)
            except (ValueError, KeyError, TypeError) as e:
                pass
            else:
                collection.insert(json_line)
    f.close()