"""
Some useful function to process text.
"""

import difflib, re
from dateutil import parser
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger

TAGS = {'LOCATION', 'ORGANIZATION', 'DATE', \
            'MONEY', 'PERSON', 'PERCENT', 'TIME'}

def initialize_tagger(DIR):
    """Given a path, return a StanfordNERTagger object."""

    NERTagger = StanfordNERTagger(
        DIR + 'StanfordNLP/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
        DIR + 'StanfordNLP/stanford-ner/stanford-ner.jar',
        encoding='utf-8')

    return NERTagger


def extract_named_entities(text):
    """
    Given some text (string), return named entities and their positions (list).
    """
    # tokenize
    tokenized_text = word_tokenize(text)
    # NER tagging
    NERTagger = initialize_tagger('/home/badr/')
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


def find_ngrams(text, N=None):
    """Given some text, return list of ngrams from n = 1 up to N (or num of tokens)."""
    tokens = word_tokenize(text)
    ngrams = []

    if N is None:
        N = len(tokens)

    for n in range(1, N + 1):
        ngrams.extend(*[zip(*[tokens[i:] for i in range(n)])])

    return ngrams

def tokenize_and_concat(text):
    """A wrapper for nltk tokenizer that returns a string."""
    return ' '.join(word_tokenize(text))


def get_capitalized(text):
    """Return a list of capitalized words in a string."""
    return [w for w in word_tokenize(text) if w[0].isupper()]


def find_best_match(entity_str, text_lex):
    """
    Given an entity string and list of ngrams that occur in the text
    lexicalization of a graph, return the ngram that is the best match.
    :para entity_str: entity (string)
    :para text_lex: text (string)
    """
    lex_ngrams = [' '.join(ngrams) for ngrams in find_ngrams(text_lex)]

    best_matches = difflib.get_close_matches(entity_str, lex_ngrams)

    return best_matches[0] if best_matches else None


def is_date_format(text):
    """Given a string, return True if date, False otherwise."""
    try:
        parser.parse(text)
        return True
    except (ValueError, OverflowError) as e:
        return False

def char_ngrams(chars, N=None):
    """Given some string, return list of character ngrams."""
    char_ngrams = []

    if N is None:
        N = len(chars)

    for n in range(2, N + 1):
        char_ngrams.extend(*[zip(*[chars[i:] for i in range(n)])])

    return char_ngrams


def generate_abbrs(text):
    """
    Given a text (entity), return a list of possible abbreviations.
    For example, generate_abbrs("United States") -- > ['U. S.', 'U.S.', 'U S', 'US']
    """
    all_inits = [w[0] for w in text.split() if not w[0].isdigit()]
    capital_inits = [w[0].upper() for w in text.split() if not w[0].isdigit()]
    init_caps_only = [c for c in all_inits if c.isupper()]

    abbrs_pool = []

    for char_set in (all_inits, capital_inits, init_caps_only):
        c_ngrams = [''.join(g) for g in char_ngrams(char_set)] + \
            [' '.join(g) for g in char_ngrams(char_set)] + \
            ['.'.join(g) + '.' for g in char_ngrams(char_set)] + \
            ['.'.join(g) for g in char_ngrams(char_set)] + \
            ['. '.join(g) + '.' for g in char_ngrams(char_set)]

        abbrs_pool.extend(c_ngrams)

    return sorted(set(abbrs_pool), key=len, reverse=True)


# pre-compile regexes for the CamelCase converting function
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camel_case_split(property_string):
    """Return the text of the property after (camelCase) split."""
    s1 = first_cap_re.sub(r'\1 \2', property_string)
    return all_cap_re.sub(r'\1 \2', s1).lower().replace('_', ' ').replace('/', ' ')

# test function
def test_date_format():
    dates = [
        "Jan 19, 1990",
        "January 19, 1990",
        "Jan 19,1990",
        "01/19/1990",
        "01/19/90",
        "1990",
        "Jan 1990",
        "January, 1990",
        "2009-6-19",
        "28th of August, 2008",
        "August 28th, 2008"
    ]

    for d in dates:
        print(d, is_date_format(d))


def test_abbrs():
    print(generate_abbrs("Massachusetts Institute, of Technology, Sc.D. 1963"))
    print(generate_abbrs("United States"))
    print(generate_abbrs("New York City"))

def test_NER():
    text = """While in France, Christine Lagarde Johnson's team discussed
        short-term stimulus efforts in a recent interview with the Wall
        Street Journal on August 1st 2017. The United Nations decided to apply
        harmless nuclear regulations on Iran. The United States of America
        has many great cities such as New York, Las Vegas, and San Francisco.
        Distinguished Service Medal from United States Navy ranks higher than
        Department of Commerce Gold Medal.""".replace('\n', '')

    E = extract_named_entities(text)

    for (e, i) in E:
        print('§', e, '§', i[0], i[1])


def test_best_match():
    entity_list = [
        "Massachusetts Institute, of Technology, Sc.D. 1963",
        "Italy",
        "Colombian cuisine",
        "United States",
        """In Soldevanahalli, Acharya Dr. Sarvapalli Radhakrishnan Road,
        Hessarghatta Main Road, Bangalore – 560090.""",
        "Dr. G. P. Prabhukumar",
        "Lars Løkke Rasmussen",
        "Prime Minister of Romania",
        "Türk Şehitleri Anıtı", "16000",
        "United States",
        "St. Louis",
        "25.0",
        "Americans",
        "Ilocano people",
        "English language",
        "Alan Shepard",
        "1971-07-01",
        "2014–15 Azerbaijan Premier League"
    ]

    text_list = [
        """Born on the twentieth of January, 1930, 1963 Massachusetts Institute
        of Technology, Sc.D. graduate Buzz Aldrin has won 20 awards.""",
        """talian born Michele Marcolini is the manager of AC Lumezzane.
        He also played for Vicenza Calcio and owns Torino FC.""",
        """A typical dish found in Columbia is Bandeja paisa, which comes
        from the Antioquia Department region.""",
        """St Vincent-St Mary High School (Akron, Ohio, US) is the ground of
        Akron Summit Assault.""",
        """Acharya Institute of Technology (motto: 'Nurturing Excellence') was
        established in 2000 and is located at Soldevanahalli, Acharya Dr.
        Sarvapalli Radhakrishnan Road, Hessarghatta Main Road, Bangalore –
        560090, Karnataka, India. The Institute is affiliated with
        Visvesvaraya Technological University of Belgaum.""",
        """The Acharya Institute of Technology's campus is located in
        Soldevanahalli, Acharya Dr. Sarvapalli Radhakrishnan Road, Hessarghatta
        Main Road, Bangalore, India, 560090. It was established in 2000 and its
        director is Dr G.P. Prabhukumar. It is affiliated to the Visvesvaraya
        Technological UNiversity in Belgaum.""",
        """The School of Business and Social Sciences at the Aarhus University
        is located in the city of Aarhus, Denmark, and is affiliated with the
        European University Association in Brussels. Aarhus is ruled by a
        magistrate government, and is led by Lars Lokke Rasmussen. The
        religion is the Church of Denmark.""",
        """The 1 Decembrie 1918 University is located in Romania and its Latin
        name is 'Universitas Apulensis'. Romania's ethnic group is the Germans
        of Romania and its leader is Prime Minister Klaus Iohannis. Romania's
        capital is Bucharest and its anthem is Desteapta-te, romane!""",
        """Baku Turkish Martyrs' Memorial, made of red granite and white marble,
        is dedicated to the Ottoman Army soldiers killed in the Battle of Baku.
        The memorial, called Turk Sehitleri Aniti, was designed by Hüseyin
        Bütüner and Hilmi Güner and is located in Azerbaijan, the capital of
        which is Baku.""",
        """The School of Business and Social Sciences is located in Aarhus and
        it was established in 1928. It has 737 academic staff and 16,000
        students. Its dean is Thomas Pallesen and it is affiliated with the
        European University Association.""",
        """Andrews County Airport is located in Texas in the U.S. Austin is the
        capital of Texas whose largest city is Houston. English is spoken
        in that state.""",
        """Elliot See was born in Dallas on 23 July 1927. He graduated from the
        University of Texas at Austin which is an affiliate of the University
        of Texas system. He died in St louis .""",
        """Aarhus Airport, which serves the city of Aarhus in Denmark, has a
        runway length of 2,776 and is named 10R/28L. Aktieselskab operates the
        airport which is 25 metres above sea level.""",
        """The character of Baymax appeared in Big Hero 6 which stars Ryan
        Potter. He was created by Steven T Seagle and the American,
        Duncan Rouleau.""",
        """Batchoy is found in Philippine Spanish and Arabic speaking
        Philippines. The Philippines is home to the llocano and ENTITY.""",
        "English is the language used in 1634: The Ram Rebellion.",
        "Alan Shephard passed away on 1998-07-21 in California.",
        """Buzz Aldrin, who retired on July 1st 1971 , once spent 52 minutes
        in outer space.""",
        """AZAL Arena, which holds 3500 fans, is the ground of AZAL PFK who
        played in the Azerbaijan Premier League in 2014-15. Qarabag FK have
        been champions of this league. """
    ]

    for (e, s) in zip(entity_list, text_list):
        best_match = find_best_match(e, s)
        print('entity:', e, ', best match:', best_match)

def main():
    # test extract_named_entities function.
    #test_NER()

    # test best match
    test_best_match()

    # test data format
    test_date_format()

    # test generate_abbrs
    test_abbrs()

if __name__ == '__main__':
    main()
