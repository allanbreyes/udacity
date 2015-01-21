"""
Exports `data/nyc.osm-street-audit.json`, used for exploratory data analysis in
preparation for data cleaning.
"""
from collections import defaultdict
from pprint import pprint
import json
import re
import xml.etree.cElementTree as ET

import suffix

OSMFILE = "data/nyc.osm"
suffix_table = suffix.SuffixTable()

def titleize(string):
    return string.title()

expected = map(titleize, suffix_table.suffixes)

def is_word(string):
    return re.match(r'\w+', string) != None

def clean_suffix(string):
    return suffix_table.convert(string.lower()).title()

def clean_street_name(street_name):
    street_name_split = re.split(r'(\W+)', street_name)
    for i in range(len(street_name_split)):
        word = street_name_split[i]
        if '.' in word:
            street_name_split[i] = word.replace('.', '')
        if is_word(word) and suffix_table.has_suffix(word):
            street_name_split[i] = clean_suffix(word)
    return ''.join(street_name_split)


def audit_street_type(street_types, street_name):
    suffix = None
    for word in re.split(r'(\W+)', street_name)[::-1]:
        if suffix_table.has_suffix(word):
            suffix = clean_suffix(word)
            break
    if suffix:
        street_type = suffix
    else:
        street_type = street_name.split()[-1]
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"

def audit(osmfile, limit=-1):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    counter = 0
    for _, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        if limit > 0 and counter > limit:
            break
        counter += 1
    return street_types

def test_audit(limit=-1):
    st_types = audit(OSMFILE, limit)
    data = dict(st_types)
    pprint(data)
    for key in data:
        data[key] = list(data[key])
    json.dump(data, open(OSMFILE + '-street-audit.json', 'w'))
    return data

if __name__ == '__main__':
    test_audit(10**7)
