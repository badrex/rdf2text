"""
For each property in the dataset, get its domain and range.
"""

from collections import defaultdict
from utils import sparql_utils
import argparse

def generate():
    """
    Read options from user input, and generate dataset.
    """

    DISCR = 'Generate schema for  properties in the RDF data.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-output', type=str, help='Path to output file.', required=True)

    args = parser.parse_args()

    with open('metadata/properties.list', encoding="utf8") as f:
        rdf_prop_list = [prop.strip() for prop in f.readlines()]

    prop_schema = []

    for (i, prop) in enumerate(rdf_prop_list):
        prop_domain = sparql_utils.get_property_domain(prop)
        prop_range = sparql_utils.get_property_range(prop)

        prop_schema.append((prop, prop_domain, prop_range))

        if i != 0 and i % 10 == 0:
            print(i, "properties processed so far ...")


    with open(args.output, '+w') as pFile:
        for (p, d, r) in prop_schema:
            pFile.write(' '.join((p, d, r)) + '\n')

def main():
    generate()

if __name__ == '__main__':
    main()
