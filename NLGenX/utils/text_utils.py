"""
Some useful function to process text.
"""

from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger

DIR = '/home/badr/'

NERTagger = StanfordNERTagger(
    DIR + 'StanfordNLP/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
    DIR + 'StanfordNLP/stanford-ner/stanford-ner.jar',
    encoding='utf-8')

TAGS = {'LOCATION', 'ORGANIZATION', 'DATE', \
            'MONEY', 'PERSON', 'PERCENT', 'TIME'}

def extract_named_entities(text):
    """
    Given a sentence (string), return named entities and their positions (list).
    """
    # tokenize
    tokenized_text = word_tokenize(text)
    # NER tagging
    tagged_text = NERTagger.tag(tokenized_text)
    # entities
    named_entities = []

    # set a previous_tag to non-entity
    previous_tag = 'O'

    for (word, tag) in tagged_text:
        if tag in TAGS:
            # if same as previous tag, concatenate with last entry
            if previous_tag == tag:
                named_entities.append(' '.join([named_entities.pop(), word]))

            else: # if not same as previous, append new entry
                named_entities.append(word)

        previous_tag = tag

    # get indicies of names entities in the text
    entity_position_list = []

    for entity in named_entities:
        start_idx = text.find(entity)
        end_idx = start_idx + len(entity)
        entity_position_list.append((entity, (start_idx, end_idx)))

    return entity_position_list


def main():
    """Test extract_named_entities function."""

    text = """While in France, Christine Lagarde Johnson's team discussed
            short-term stimulus efforts in a recent interview with the Wall
            Street Journal on August 1st 2017. The United Nations decided to
            apply harmless nuclear regulations on Iran.
            The United States of America has many great cities such as
            New York, Las Vegas, and San Francisco."""

    E = extract_named_entities(text)

    for (e, i) in E:
        print(e, i[0], i[1]) # text[i[0]: i[1]]

if __name__ == '__main__':
    main()
