"""
A program to generate a list of entities which could not be delex.
NOTE: Only for testing purposes.
"""

from utils import rdf_utils
import argparse
from graph2text import *

def generate():
    """
    Read options from user input, and generate list.
    """

    DISCR = 'Generate list of entities from XML files of RDF to Text Entries.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to data.', required=True)
    parser.add_argument('-output', help='Path to output file.', required=True)

    args = parser.parse_args()

    instances, _, _ = rdf_utils.generate_instances(args.path)

    not_delex = set()

    counter = 0
    for (size, ins) in instances.items():
        for i in ins:
            tripleset = (i.originaltripleset, i.modifiedtripleset)
            G = FactGraph(tripleset, i.Lexicalisation.lex)
            _, nodelex = G.delexicalize_text(advanced=True)

            not_delex.update(nodelex)
            counter += 1

            if counter % 10 == 0:
                print("Processed so far: ", counter)

    print(len(not_delex))

    with open(args.output, 'w+', encoding="utf8") as opFile:
        opFile.write("\n".join(str(e) + ' § ' + str(s) for (e, s) in not_delex))


def main():
    generate()

if __name__ == '__main__':
    main()
