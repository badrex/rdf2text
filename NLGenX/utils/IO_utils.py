"""
Some useful functions and data structures to read and process XML files.
"""

import xml.etree.ElementTree as et
from collections import defaultdict
from . import rdf_utils
import argparse
import os


class RDFInstance(object):

    def __init__(self, category, size, otripleset, mtripleset, lex=None):
        """
        Instantiate RDFInstance object.
        :param category: category of entry (dtype: string)
        :param size: number of triples in entry (dtype: int)
        :param otripleset: a list original tripleset (dtype: list (Tripleset))
        :param mtripleset: a modified tripleset (dtype: Tripleset)
        :param sentence: a sentence that realises the triple set for training
        instances
            :dtype: Lexicalisation object (to get text, Lexicalisation.lex)
            :default: None (for eval and test instances).
        """

        self.category = category
        self.size = size
        self.originaltripleset = otripleset
        self.modifiedtripleset = mtripleset

        if lex:
            self.Lexicalisation = lex


def parseXML(xml_file):
    """
    Parse an xml file, return a list of RDF-Text instances (list(Entry)).
    :param category: xml_file string (dtype: string)
    """

    entries = []

    tree = et.parse(xml_file)
    root = tree.getroot()

    for xml_entry in root.iter('entry'):
        # to ignore triples with no lexicalisations
        # get a list of tags in the entry
        tags = [c.tag for c in xml_entry]

        if "lex" not in tags:
            # skip this entry, move to next entry in the loop
            continue

        # get attributes
        entry_id = xml_entry.attrib['eid']
        category = xml_entry.attrib['category']
        size = xml_entry.attrib['size']

        entry = rdf_utils.Entry(category, size, entry_id)

        for element in xml_entry:
            if element.tag == 'originaltripleset':
                entry.fill_originaltriple(element)
            elif element.tag == 'modifiedtripleset':
                entry.fill_modifiedtriple(element)
            elif element.tag == 'lex':
                entry.create_lex(element)

        entries.append(entry)

    return entries


def generate_instances(dir):
    """
    Traverse through a path, visit all subdirectories, and return a dict of
    entries accessible by size: size --> list of entries
    """
    subfolders = [f.path for f in os.scandir(dir) if f.is_dir() ]

    instances = defaultdict(list)

    # loop through each dir
    for dir in sorted(subfolders):
        xml_files = [f for f in os.listdir(dir) if f.endswith('.xml')]

        # loop through each file in the directory
        for f in xml_files:
            # create new XMLParser object
            entries = parseXML(dir + '/' + f)

            for entry in entries:
                for lex in entry.lexs:
                    rdfInstance = RDFInstance(entry.category,
                                    entry.size,
                                    entry.originaltripleset,
                                    entry.modifiedtripleset,
                                    lex)

                    # append to list of instances
                    instances[entry.size].append(rdfInstance)

    return instances
