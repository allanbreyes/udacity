#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from pprint import pprint
import xml.etree.ElementTree as ET

FILE_IN = 'data/austin.osm'
FILE_OUT = 'data/austin-subset.osm'


def main(file_in, file_out):
    """ main routine """
    root = ET.Element('osm')
    counter = 0

    for _, elem in ET.iterparse(file_in, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            tag_type = elem.tag
            if len([child.tag for child in elem.iter("tag")]) >= 5:
                print '.',
                node = ET.SubElement(root, tag_type, attrib=elem.attrib)
                for tag in elem.iter("tag"):
                    child = ET.SubElement(node, 'tag', attrib=tag.attrib)

    tree = ET.ElementTree(root)
    tree.write(file_out)

if __name__ == '__main__':
    main(FILE_IN, FILE_OUT)
