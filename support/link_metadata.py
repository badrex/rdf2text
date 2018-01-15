"""
A program to link metadata (e.g. size, category) to lexicalised predictions
for evaluation and testing.
"""

import argparse

def link():
    """
    Read options from user input, and generate eval dataset.
    """

    DISCR = 'Link metadata to predictions.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-pred', type=str, help='Path to preditions.',
                    required=True)

    parser.add_argument('-meta', type=str, help='Path to metadata.',
                    required=True)

    parser.add_argument('-output', type=str, help='Path to output file.',
                    required=True)

    args = parser.parse_args()

    with open(args.pred, 'r', encoding="utf8") as predFile:
        predictions = predFile.readlines()

    with open(args.meta, 'r', encoding="utf8") as metaFile:
        metadata = metaFile.readlines()


    for (d, p) in zip(metadata, predictions):
            # write to a file
            print(d, p)
            with open(args.output, 'a+', encoding="utf8") as outputFile:
                d = [i.replace('\n', '') for i in d.split()]
                d.append(p.replace('\n', ''))
                outputFile.write('\t'.join([j for j in d])  + '\n')


def main():
    link()

if __name__ == '__main__':
    main()
