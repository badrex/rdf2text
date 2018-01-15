"""
This module contains some useful classes and functions to deal with RDF data and
read and process XML files.
"""

from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as et
from collections import defaultdict
import argparse
import os


class Triple:

    def __init__(self, s, p, o):
        self.subject = s
        self.object = o
        self.property = p


class Tripleset:

    def __init__(self):
        self.triples = []

    def fill_tripleset(self, t):
        for xml_triple in t:
            s, p, o = xml_triple.text.split(' | ')

            # inistiate a triple
            triple = Triple(s, p, o)
            self.triples.append(triple)


class Lexicalisation:

    def __init__(self, lex, comment, lid):
        self.lex = lex
        self.comment = comment
        self.id = lid


class Entry:

    def __init__(self, category, size, eid):
        self.originaltripleset = []
        self.modifiedtripleset = Tripleset()
        self.lexs = []
        self.category = category
        self.size = size
        self.id = eid

    def fill_originaltriple(self, xml_t):
        otripleset = Tripleset()
        self.originaltripleset.append(otripleset)   # multiple originaltriplesets for one entry
        otripleset.fill_tripleset(xml_t)

    def fill_modifiedtriple(self, xml_t):
        self.modifiedtripleset.fill_tripleset(xml_t)

    def create_lex(self, xml_lex):
        comment = xml_lex.attrib['comment']
        lid = xml_lex.attrib['lid']
        lex = Lexicalisation(xml_lex.text, comment, lid)
        self.lexs.append(lex)

    def count_lexs(self):
        return len(self.lexs)


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

        self.entities = set()
        self.properties = set()

        self._populate_sets()


    def _populate_sets(self):
        """
        populate the two sets; entities and properties.
        """
        for tset in self.originaltripleset:
            for triple in tset.triples:
                s = triple.subject
                p = triple.property
                o = triple.object

                self.entities.update((s, o))
                self.properties.add(p)


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

        entry = Entry(category, size, entry_id)

        for element in xml_entry:
            if element.tag == 'originaltripleset':
                entry.fill_originaltriple(element)
            elif element.tag == 'modifiedtripleset':
                entry.fill_modifiedtriple(element)
            elif element.tag == 'lex':
                entry.create_lex(element)

        entries.append(entry)

    return entries


def generate_instances(dir, extended=False, eval=False):
    """
    Traverse through a path, visit all subdirectories, and return a dict of
    entries accessible by size: size --> list of entries
    :param dir: path to data files (dtype: string)
    :param extended: should it generate entities and properties?
        (dtype: bool, default: False)
    """

    subfolders = [f.path for f in os.scandir(dir) if f.is_dir() ]

    instances = defaultdict(list)

    global_entities = set()
    global_properties = set()

    # loop through each dir
    for d in sorted(subfolders):
        xml_files = [f for f in os.listdir(d) if f.endswith('.xml')]

        # loop through each file in the directory
        for f in xml_files:
            # create new XMLParser object
            entries = parseXML(d + '/' + f)

            if eval:
                for entry in entries:
                    rdfInstance = RDFInstance(entry.category,
                                entry.size,
                                entry.originaltripleset,
                                entry.modifiedtripleset,
                                entry.lexs)

                    # append to list of instances
                    instances[entry.size].append(rdfInstance)

                    if extended:
                        global_entities.update(rdfInstance.entities)
                        global_properties.update(rdfInstance.properties)

            else:
                for entry in entries:
                    for lex in entry.lexs:
                        rdfInstance = RDFInstance(entry.category,
                                        entry.size,
                                        entry.originaltripleset,
                                        entry.modifiedtripleset,
                                        lex)

                        # append to list of instances
                        instances[entry.size].append(rdfInstance)

                        if extended:
                            global_entities.update(rdfInstance.entities)
                            global_properties.update(rdfInstance.properties)

    return instances, global_entities, global_properties
