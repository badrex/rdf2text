"""
A program to process RDF data and generate metadata (e.g. size, category)
for evaluation and testing.
"""

from utils import rdf_utils
import argparse
from graph2text import *

def generate():
    """
    Read options from user input, and generate eval dataset.
    """

    DISCR = 'Generate dataset from XML files of RDF to Text Entries.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to tgt data.',
                    required=True)

    parser.add_argument('-seen', type=str, help='SEEN or UNSEEN.',
                    required=True)

    parser.add_argument('-output', type=str, help='Path to output file.',
                    required=True)

    args = parser.parse_args()

    instances, _, _ = rdf_utils.generate_instances(args.path, eval=True)

    counter = 1

    for (size, ins) in instances.items():
        for i in ins:
            id = counter
            size = i.size
            cat = i.category

            mdata = [id, int(size), cat, args.seen]

            print(mdata)

            # write to a file
            with open(args.output, 'a+', encoding="utf8") as outputFile:
                outputFile.write('\t'.join(str(j) for j in mdata)  + '\n')

            counter += 1


def main():
    generate()

if __name__ == '__main__':
    main()
