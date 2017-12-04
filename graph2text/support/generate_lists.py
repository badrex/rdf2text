"""
A program to process RDF data and generate lists of entities and properties.
"""

from utils import rdf_utils
import argparse
import os


def generate():
    """
    Read options from user input, and generate dataset.
    """

    DISCR = 'Generate lists of entities and properties from RDF data.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to data.', required=True)

    parser.add_argument('-entity_list', type=str, help='Path to entities file.',
                    required=True)
    parser.add_argument('-prop_list', type=str, help='Path to properties file.',
                    required=True)

    args = parser.parse_args()

    subdirs = [f.path for f in os.scandir(args.path) if f.is_dir()]

    e_list = set()
    p_list = set()

    for data_dir in subdirs:
        _, entities, properties = rdf_utils.generate_instances(data_dir, True)
        e_list.update(entities)
        p_list.update(properties)

        print(data_dir, len(entities), len(properties))
        print(data_dir, len(e_list), len(p_list))

    print(len(e_list), len(p_list))

    with open(args.entity_list, '+a') as eFile:
        eFile.write("\n".join(e_list))

    with open(args.prop_list, '+a') as pFile:
        pFile.write("\n".join(p_list))


def main():
    generate()

if __name__ == '__main__':
    main()
