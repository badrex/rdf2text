"""
For each property in the dataset, get its domain and range.
"""

from collections import defaultdict
from utils import sparql_utils
import argparse

def generate():
    """
    Read options from user input, and generate output.
    """

    DISCR = 'Get semantic type for entities in the RDF data.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-output', type=str, help='Path to output file.', required=True)

    args = parser.parse_args()

    with open('metadata/entities.list', encoding="utf8") as f:
        rdf_entity_list = [e.strip() for e in f.readlines()]

    entity_type = []

    for (i, e) in enumerate(rdf_entity_list):
        stype = sparql_utils.get_resource_type(e)

        entity_type.append((e, stype))

        if i != 0 and i % 10 == 0:
            print(i, "entities processed so far ...")


    with open(args.output, '+w') as pFile:
        for (e, stype) in entity_type:
            pFile.write(' '.join((e, stype)) + '\n')

def main():
    generate()

if __name__ == '__main__':
    main()
