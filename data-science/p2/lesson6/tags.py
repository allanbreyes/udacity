#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        key = element.get("k")
        print key,
        # value = element.get("v")
        if problemchars.search(key):
            keys['problemchars'] += 1
            print '--> problemchars'
        elif lower_colon.search(key):
            keys['lower_colon'] += 1
            print '--> lower_colon'
        elif lower.search(key):
            keys['lower'] += 1
            print '--> lower'
        else:
            keys['other'] += 1
            print '--> other'
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()