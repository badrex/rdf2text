"""
A program to process RDF data and generate dataset for training.
"""

from utils import rdf_utils
import argparse
from graph2text import *

def generate():
    """
    Read options from user input, and generate dataset.
    """

    DISCR = 'Generate dataset from XML files of RDF to Text Entries.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to data.', required=True)
    parser.add_argument('-src_mode', help='source mode: flat or structured.',
                choices=['flat', 'structured'], default = 'flat', nargs = '?')

    parser.add_argument('-delex_mode', type=str, help='Advanced or simple delexicalization',
                choices=['simple', 'adv'], default = 'adv', nargs = '?')

    parser.add_argument('-src', type=str, help='Path to output file for src.',
                    required=True)
    parser.add_argument('-tgt', type=str, help='Path to output file for tgt.',
                    required=True)

    args = parser.parse_args()

    instances, _, _ = rdf_utils.generate_instances(args.path)

    for (size, ins) in instances.items():
        for i in ins:
            tripleset = (i.originaltripleset, i.modifiedtripleset)
            G = FactGraph(tripleset, i.Lexicalisation.lex)

            with open(args.src, 'a+', encoding="utf8") as srcFile:
                if args.src_mode == 'structured':
                    srcFile.write(G.linearize_graph(structured=True, incoming_edges=True) + '\n')
                else:
                    srcFile.write(G.linearize_graph() + '\n')

            # write tgt
            adv_delex = False if args.delex_mode == 'simple' else True

            with open(args.tgt, 'a+', encoding="utf8") as tgtFile:
                tgtFile.write(G.delexicalize_text(adv_delex).replace('\n', ' ')  + '\n')


def main():
    generate()

if __name__ == '__main__':
    main()
