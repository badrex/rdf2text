"""
A module for RDF Entity, RDF Property, and FactGraph.
"""

from utils import text_utils, rdf_utils, sparql_utils
import xml.etree.ElementTree as et
import re
import string
from collections import defaultdict


# populate a dict for schema properties: prop --> (domain, range)
prop2schema = {}

with open('metadata/prop_schema.list', encoding="utf8") as f:
    for line in f.readlines():
        (p, d, r) = line.strip().split()
        prop2schema[p] = (d, r)

# populate a dict for semantic types of entities: entity --> type
entity2type = {}

with open('metadata/entity_type.list', encoding="utf8") as f:
    for line in f.readlines():
        last_space_idx = line.rfind(' ')
        entity = line[:last_space_idx]
        stype = line[last_space_idx:]

        hash_idx = stype.find('#')
        stype = stype[hash_idx + 1:]

        entity2type[entity] = stype.strip()


class RDFEntity:
    """ A class to represent an RDF entity. """

    def __init__(self, ID, o_rdf_entity, m_rdf_entity, semantic_type=None):
        """
        Instantiate an entity.
        :param o_rdf_entity: original entity from an RDF triple (dtype: string)
        :param m_rdf_entity: modified entity from an RDF triple (dtype: string)
        """
        self.ID = 'ENTITY_' + str(ID)

        # the join function is used to substitute multiple spaces with only one
        self.olex_form = ' '.join(self.text_split(o_rdf_entity).split())
        self.mlex_form = ' '.join(self.text_split(m_rdf_entity).split())

        if semantic_type is None:
            self.stype = entity2type[o_rdf_entity]
        else:
            hash_idx = semantic_type.find('#')
            semantic_type = semantic_type[hash_idx + 1:]
            self.stype = semantic_type

        self.aliases = self.get_aliases()

    def text_split(self, entity_str):
        """Return the text of the entity after split."""
        return ' '.join(entity_str.split('_'))

    def get_aliases(self):
        """Return a list of aliases for the entity."""
        # TODO: find a way to retrieve a list of aliases for an entity from
        # (for example) an online resource
        return [self.mlex_form, self.mlex_form.lower()]

    def set_stype(self, semantic_type):
        """Given a semantic_type, modify self.stype."""
        self.stype = semantic_type


class RDFProperty:
    """ A class to represent RDF property (predicate). """

    def __init__(self, o_rdf_property, m_rdf_property):
        """
        Instantiate a property.
        :param o_rdf_property: original prop from an RDF triple (dtype: string)
        :param o_rdf_property: modified prop from an RDF triple (dtype: string)
        """
        self.olex_form = self.text_split(o_rdf_property)
        self.mlex_form = self.text_split(m_rdf_property)
        self.type_form = o_rdf_property.upper()
        self.domain = prop2schema[o_rdf_property][0]
        self.range = prop2schema[o_rdf_property][1]

    def text_split(self, property_string):
        """Return the text of the property after (camelCase) split."""
        return text_utils.camel_case_split(property_string)


class FactGraph:
    """
    A class to represent RDF graph instances for natural language generation
    from structed input (e.g. RDF triples from a knowledge base).
    NOTE: Training instances are represented as (graph, text) pairs, while eval
    and test instances are represented only as graphs.
    """

    def __init__(self, tripleset_tuple, lexicalization=None):
        """
        Initialize and construct a graph from RDF triples.
        :param rdf_triples: a set of structured RDF triples (dtype: Tripleset)
        :param lexicalization: a text that realises the triple set for training
        instances
            :dtype: string
            :default: None (for eval and test instances).
        """

        # a set of RDF triples
        otripleset, mtripleset = tripleset_tuple
        # original
        self.o_rdf_triples = otripleset[0].triples

        # modified
        self.m_rdf_triples = mtripleset.triples

        assert len(self.o_rdf_triples) == len(self.m_rdf_triples), \
            "Original and modified tripleset are not the same length."

        # for training instances, initilize the corresponding lexicalization
        if lexicalization:
            self.lexicalization = lexicalization

        # a dict for entities in the graph instance
        # this dict maps from lex_form of entity to entity object
        self.entities = {}

        # id2entity dict is used for relexicalization for eval datasets
        self.id2entity = {}

        # a dict for properties in the graph instance
        # this dict maps from lex_form of property to property object
        self.properties = {}

        # call contruct_graph() method to build the graph from the RDF triples

        # two dicts to link entities in the graph instance (subj --> (prop, obj))
        # and (obj --> (prop, subj))
        # these data structures make easy to generate structured sequences
        self.subj2obj = {}
        self.obj2subj = {}

        # call method to construct entity graph and populate other dicts
        self._contruct_graph()

    def _contruct_graph(self):
        """
        Build the graph.
        Populate entities, properties, subj2obj, and obj2subj dicts.
        """
        entityID = 0

        # loop through each zipped triple
        for (otriple, mtriple) in zip(self.o_rdf_triples, self.m_rdf_triples):
            # extract nodes (entities) and edges (properties) from original
            o_subj = otriple.subject
            o_obj = otriple.object
            o_prop = otriple.property

            # extract nodes (entities) and edges (properties) from modified
            m_subj = mtriple.subject
            m_obj = mtriple.object
            m_prop = mtriple.property

            # update properties dict by instantiating RDFProperty objects
            if o_prop not in self.properties:
                self.properties[o_prop] = RDFProperty(o_prop, m_prop)

            # update entities dict by instantiating RDFEntity objects
            if o_subj not in self.entities:
                entityID += 1
                # first try to use the domain of the property
                if self.properties[o_prop].domain != '*':
                    self.entities[o_subj] = RDFEntity(entityID, o_subj, m_subj,
                                            self.properties[o_prop].domain)

                # directly retrieve the type of the subj
                else:
                    self.entities[o_subj] = RDFEntity(entityID, o_subj, m_subj)

                # add to id2entity dicr
                self.id2entity[entityID] = self.entities[o_subj].mlex_form

            if o_obj not in self.entities:
                entityID += 1
                # we first try to use the range of the property
                if self.properties[o_prop].range != '*':
                    self.entities[o_obj] = RDFEntity(entityID, o_obj, m_obj,
                                            self.properties[o_prop].range)

                # try to directly retrieve the type of the obj
                else:
                    self.entities[o_obj] = RDFEntity(entityID, o_obj, m_obj)

                    # if the stype is 'THING', use the expression of the prop as a type
                    if self.entities[o_obj].stype == 'THING':
                        self.entities[o_obj].set_stype(self.properties[o_prop].type_form)

                # add to id2entity dicr
                self.id2entity[entityID] = self.entities[o_obj].mlex_form

            # populate the subj2obj and obj2subj dicst with (prop, [objs]) or
            # (prop, [subjs]) tuples
            # flag var to check if the property already added to a node
            propFound = False

            # TODO: make FIRST and SECOND blocks more elegant
            # FIRST: populate subj2obj
            if o_subj not in self.subj2obj:
                self.subj2obj[o_subj] = [(o_prop, [o_obj])]
             # if subj entity already seen in the graph
            else:
                # we need to do something smart now
                # loop through all already added (prob, [obj]) tuples
                for i, (p, o) in enumerate(self.subj2obj[o_subj]):
                    # if the prop already exists, append to the list of object
                    if p == o_prop:
                        propFound = True
                        # get the list and append to it
                        self.subj2obj[o_subj][i][1].append(o_obj)
                        break
                # if the search failed, add a new (prop, [obj]) tuple
                if not propFound:
                    self.subj2obj[o_subj].append((o_prop, [o_obj]))

            # SECOND: populate obj2subj
            # flag var to check if the property already added to a node
            propFound = False

            if o_obj not in self.obj2subj:
                self.obj2subj[o_obj] = [(o_prop, [o_subj])]
             # if subj entity already seen in the graph
            else:
                # we need to do something smart now
                # loop through all already added (prob, [subj]) tuples
                for i, (p, s) in enumerate(self.obj2subj[o_obj]):
                    # if the prop already exists, append to the list of object
                    if p == o_prop:
                        propFound = True
                        self.obj2subj[o_obj][i][1].append(o_subj)
                        break

                # if the search failed, add a new (prop, [obj]) tuple
                if not propFound:
                    self.obj2subj[o_obj].append((o_prop, [o_subj]))


    def delexicalize_text(self, advanced=False):
        """
        Apply delexicalization on text. Return delexicaled text.
        :para advanced: turn on advanced string similarity procedure
            (dtype: bool, default: False)
        """
        no_match_list = []
        original_text = ' '.join(re.sub('\s+',' ', self.lexicalization).split())
        delex_text = original_text

        # loop over each entity, find its match in the text
        for entity in self.entities.values():
            # flag var, set to True if the procedure finds a match
            matchFound = False

            # remove quotes from the entity string
            entity_str = entity.mlex_form.replace('"', '')

            # Simple text matching
            # 1. try exact matching 1258
            if entity_str in self.lexicalization:
                delex_text = delex_text.replace(entity_str,
                                ' ' + entity.ID + ' ')
                matchFound = True

            # 2. try lowercased search 1122
            elif entity_str.lower() in self.lexicalization.lower():
                start_idx = delex_text.lower().find(entity_str.lower())
                end_idx = start_idx + len(entity_str)

                delex_text = delex_text[:start_idx] + ' ' \
                                + entity.ID + ' ' +  delex_text[end_idx + 1:]
                matchFound = True

            # 3. Try handling entities with the subtring (semanticType) 1006
            # e.g. Ballistic (comicsCharacter) --> Ballistic
            elif entity_str.endswith(')'):
                left_idx = entity_str.find('(')

                entity_str = entity_str[:left_idx].strip()

                if entity_str in self.lexicalization:
                    delex_text = delex_text.replace(entity_str,
                                    ' ' + entity.ID + ' ')
                    matchFound = True


            # if search succeeded, go to next entity, otherwise keep searching
            if matchFound or not advanced:
                continue

            # simple search not succeeded, do non-trivial text matching
            # 4. try date format handling
            if text_utils.is_date_format(entity_str):
                entity_ngrams = text_utils.find_ngrams(self.lexicalization)

                entity_ngrams = [text_utils.tokenize_and_concat(' '.join(ngram))
                                    for ngram in entity_ngrams]

                date_strings = [d_str for d_str in entity_ngrams
                                    if text_utils.is_date_format(d_str)]

                # sort data strings by length, get the longest match
                date_strings.sort(key=len, reverse=True)

                if date_strings:
                    best_match = date_strings[0]
                    delex_text = text_utils.tokenize_and_concat(delex_text)
                    delex_text = delex_text.replace(best_match, ' ' + entity.ID + ' ')

                    matchFound = True

            # 5. try abbreviation handling
            # if entity_str contains more than one capitalized word, try to find
            # a potential abbreviation of it in the text
            if len(text_utils.get_capitalized(entity_str)) > 1 and not matchFound:
                # from the entity string, make a list of possible abbreviations
                abbr_candidates = text_utils.generate_abbrs(entity_str)
                abbr_candidates.sort(key=len, reverse=True)

                # get a list of unigrams in the text sentence
                text_unigrams = text_utils.find_ngrams(self.lexicalization, N=1)
                text_unigrams = [' '.join(unigram) for unigram in text_unigrams]

                for abbr in abbr_candidates:
                    # make sure candidate abbr contains more than 1 capital letter
                    nCaps = len([c for c in abbr if c.isupper()])

                    if abbr in text_unigrams and nCaps > 1: # SUCCESS
                        print('before:', entity_str, abbr, delex_text)
                        delex_text = delex_text.replace(abbr, ' ' + entity.ID + ' ')
                        print('after:', entity_str, abbr, delex_text)
                        matchFound = True

            # 6. try character-level string matching (last hope)
            if not matchFound:
                delex_text = text_utils.tokenize_and_concat(delex_text)
                best_match = text_utils.find_best_match(entity_str, delex_text)

                if best_match:
                    delex_text = delex_text.replace(best_match,
                                    ' ' + entity.ID + ' ')

                    matchFound = True

            if not matchFound:
                no_match_list.append((entity_str, self.lexicalization))

        final_delex = text_utils.tokenize_and_concat(delex_text)

        # make sure the text ends with a period
        final_delex = final_delex if final_delex[-1] == '.' else final_delex + ' .'

        return  final_delex # , no_match_list


    def get_entityGraph(self):
        """
        Return a dict of entities and thier outgoing edges.
        """
        return self.subj2obj


    def linearize_graph(self, structured=False, incoming_edges=False):
        """
        Generate a linear sequence representing the graph from the triple set
        (flat sequence) or from the entity graphs (structured sequence).
        """

        if not structured:
            seq = ''

            # to generate a flat sequence, linearize rdf_triples
            for triple in self.o_rdf_triples:
                # extract nodes (entities) and edges (properties)
                subj = triple.subject
                obj = triple.object
                prop = triple.property

                seq = ' '.join(
                                [
                                    seq,
                                    self.entities[subj].ID,
                                    self.entities[subj].stype,
                                    self.properties[prop].mlex_form,
                                    self.entities[obj].ID,
                                    self.entities[obj].stype,
                                ]
                            )
        else:
            # to generate a structured sequence, linearize entity graphs
            if incoming_edges:
                entityGraph = self.obj2subj
            else:
                entityGraph = self.subj2obj

            seq = '('

            for (attr, val) in entityGraph.items():
                seq = ' '.join([seq, '('])
                seq = ' '.join(
                                [
                                    seq,
                                    self.entities[attr].ID,
                                    self.entities[attr].stype
                                ]
                           )

                for prop, obj_list in val:
                    seq = ' '.join([seq, '(', self.properties[prop].mlex_form])

                    for obj in obj_list:
                        seq = ' '.join(
                                        [
                                            seq,
                                            '(',
                                            self.entities[obj].ID,
                                            self.entities[obj].stype,
                                            ')'
                                        ]
                                    )
                    seq = ' '.join([seq, ')'])
                seq = ' '.join([seq,  ')'])
            seq = ' '.join([seq, ')'])

        return seq.lstrip()


def test():
    xml_str = """<triples>
                    <otriple>Donald Trump | birthPlace | USA</otriple>
                    <otriple>USA | leaderName | Donald Trump</otriple>
                    <otriple>USA | capital | Washington DC</otriple>
                    <otriple>Donald Trump | spouse | Melania Knauss</otriple>
                    <otriple>Melania Knauss | nationality | Slovenia</otriple>
                    <otriple>Melania Knauss | nationality | USA</otriple>
                    <otriple>Melania Knauss | birthDate | "1923-11-18"</otriple>
                </triples>"""

    otriple_set = et.fromstring(xml_str)
    mtriple_set = et.fromstring(xml_str)

    s = """Donald Trump was born in the United States of Amercia,
        the country where he later became the president . The captial of the US
        is Washington DC . Donald Trump 's wife , Melania Knauss , has two
        nationalities ; American and Slovenian . Melania was
        born on 18th of November 1923 .""".replace('\n', '')

    t_org = rdf_utils.Tripleset()
    t_org.fill_tripleset(otriple_set)

    t_mod = rdf_utils.Tripleset()
    t_mod.fill_tripleset(otriple_set)

    test_case = FactGraph(([t_org], t_mod), s)

    print('Properties: ', [*test_case.properties])
    print('Entities: ', [*test_case.entities])
    print('subj2obj Graph: ', test_case.subj2obj)
    print('obj2subj Graph: ', test_case.obj2subj)
    print('Linearization: ', test_case.linearize_graph())
    print('Strucutred [1]:',
        test_case.linearize_graph(structured=True))
    print('Strucutred [2]:',
        test_case.linearize_graph(structured=True, incoming_edges=True))

    delex = test_case.delexicalize_text(advanced=True)
    print('Lexicalisation:', delex)

    for p in test_case.properties.values():
        print(p.mlex_form, p.type_form, p.domain, p.range)

    assert test_case.entities.keys() == \
        {'Donald Trump', 'USA', 'Washington DC', 'Melania Knauss', \
            'Slovenia', '"1923-11-18"'}, \
        "Test case failed! Entities do not match."

    assert test_case.properties.keys() == \
        {'leaderName', 'birthPlace', 'capital', 'spouse', 'nationality', 'birthDate'}, \
        "Test case failed! Properties do not match."

    assert test_case.subj2obj == \
        {'Donald Trump': [
            ('birthPlace', ['USA']),
            ('spouse', ['Melania Knauss'])
            ],
        'USA': [
            ('leaderName', ['Donald Trump']),
            ('capital', ['Washington DC'])
            ],
        'Melania Knauss': [
            ('nationality', ['Slovenia', 'USA']),
            ('birthDate', ['"1923-11-18"'])
            ]
        }, "Test case failed! entityGraph does not match."

    print('\nTesting SUCCESSFUL!')

def main():
    test()

if __name__ == '__main__':
    main()
