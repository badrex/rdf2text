"""
A module for Entity, Property, and EntityGraph! It is fun ;-)
"""
from utils import text_utils
from utils import rdf_utils
import xml.etree.ElementTree as et
import re
import string


class Entity:
    """ A class to represent an RDF entity. """

    def __init__(self, entity_ID, RDF_entity, semantic_type='UNK'):
        """
        Instantiate an entity.
        :param RDF_entity: an entity from an RDF triple (dtype: string)
        """
        self.ID = 'ENTITY_' + str(entity_ID)

        # the join function is used to substitute multiple spaces with only one
        self.lex_form = ' '.join(self.text_split(RDF_entity).split())
        self.stype = semantic_type
        self.aliases = self.get_aliases()

    def text_split(self, RDF_entity):
        """Return the text of the entity after split."""
        return ' '.join(RDF_entity.split('_'))

    def get_aliases(self):
        """Return a list of aliases for the entity."""
        # TODO: find a way to retrieve a list of aliases for an entity from
        # (for example) an online resource
        return [self.lex_form, self.lex_form.lower()]

    def set_stype(self, semantic_type):
        """Given a semantic_type, modify self.stype."""
        self.stype = semantic_type


# (DONE) IDEA: structure entity as a dict of entity[lex_form] --> entityObject

class Property:
    """ A class to represent RDF property (predicate). """

    def __init__(self, RDF_property):
        """
        Instantiate a property.
        :param RDF_property: a property from an RDF triple (dtype: string)
        """
        self.lex_form = self.text_split(RDF_property)

        # TODO: Find a way to get the domain and range from DBpedia
        self.domain = 'AGENT'
        self.range = 'PATIENT'

    def text_split(self, RDF_entity):
        """Return the text of the property after (camelCase) split."""
        return ' '.join(RDF_entity.split('_'))


class EntityGraph:
    """
    A class to represent RDF to Text instances for natural language generation
    from structed input (e.g. knowledge base RDF triples).
    NOTE: Training instances are represented as (graph, text) pairs, while eval
    and test instances are represented only as graphs.
    """

    def __init__(self, tripleset, sentence=None):
        """
        Initialize and construct a graph or (graph, text) pair.
        :param rdf_triples: a set of structured RDF triples (dtype: Tripleset)
        :param sentence: a sentence that realises the triple set for training
        instances
            :dtype: string
            :default: None (for eval and test instances).
        """

        # a set of RDF triples
        self.rdf_triples = tripleset.triples

        # for training instances, initilize the corresponding sentence
        if sentence:
            self.sentence = sentence

        # a dict for entities in the graph instance
        # this dict maps from lex_form of entity to entity object
        self.entities = {}

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

        # (DONE) TODO: maybe move this somewhere else!!!
        # moved to the class Property


    def _contruct_graph(self):
        """
        Build the graph.
        Populate entities, properties, subj2obj and obj2subj dicts.
        """
        entityID = 0

        # loop through each triple
        for triple in self.rdf_triples:
            # extract nodes (entities) and edges (properties)
            subj = triple.subject
            obj  = triple.object
            prop = triple.property

            # update properties dict by instantiating Property objects
            if prop not in self.properties:
                self.properties[prop] = Property(prop)

            # update entities dict by instantiating Entity objects
            if subj not in self.entities:
                entityID += 1
                self.entities[subj] = Entity(entityID, subj,
                                          self.properties[prop].domain)

            if obj not in self.entities:
                entityID += 1
                self.entities[obj]  = Entity(entityID, obj,
                                          self.properties[prop].range)

            # populate the subj2obj and obj2subj dicst with (prop, [objs]) or
            # (prop, [subjs]) tuples
            # flag var to check if the property already added to a node
            propFound = False

            # TODO: make FIRST and SECOND blocks more elegant
            # FIRST: populate subj2obj
            if subj not in self.subj2obj:
                self.subj2obj[subj] = [(prop, [obj])]
             # if subj entity already seen in the graph
            else:
                # we need to do something smart now
                # loop through all already added (prob, [obj]) tuples
                for i, (p, o) in enumerate(self.subj2obj[subj]):
                    # if the prop already exists, append to the list of object
                    if p == prop:
                        propFound = True
                        # get the list and append to it
                        self.subj2obj[subj][i][1].append(obj)
                        break
                # if the search failed, add a new (prop, [obj]) tuple
                if not propFound:
                    self.subj2obj[subj].append((prop, [obj]))

            # SECOND: populate obj2subj
            # flag var to check if the property already added to a node
            propFound = False

            if obj not in self.obj2subj:
                self.obj2subj[obj] = [(prop, [subj])]
             # if subj entity already seen in the graph
            else:
                # we need to do something smart now
                # loop through all already added (prob, [subj]) tuples
                for i, (p, s) in enumerate(self.obj2subj[obj]):
                    # if the prop already exists, append to the list of object
                    if p == prop:
                        propFound = True
                        self.obj2subj[obj][i][1].append(subj)
                        break
                # if the search failed, add a new (prop, [obj]) tuple
                if not propFound:
                    self.obj2subj[obj].append((prop, [subj]))

    def delexicalize_text(self, advanced=False):
        """
        Apply delexicalization on text. Return delexicaled text.
        :para advanced: turn on advanced string similarity procedure
            (dtype: bool)
            (default: False)
        """
        no_match_list = []
        original_text = ' '.join(re.sub('\s+',' ', self.sentence).split())
        delex_text = original_text

        # loop over each entity, find its match in the text
        for entity in self.entities.values():
            # remove qouts from the entity string
            matchFound = False
            entity_string = entity.lex_form.replace('"', '')

            # Simple text matching
            # 1. try exact matching 1258
            if entity_string in self.sentence:
                delex_text = delex_text.replace(entity_string,
                                ' ' + entity.ID + ' ')
                matchFound = True

            # 2. try lowercased search 1122
            elif entity_string.lower() in self.sentence.lower():
                start_idx = delex_text.find(entity_string.lower())
                end_idx = start_idx + len(entity_string)

                delex_text = delex_text[:start_idx] + ' ' \
                                + entity.ID + ' ' +  delex_text[end_idx + 1:]
                matchFound = True


            # 3. Try handling entities with the subtring (semanticType) 1006
            # e.g. Ballistic (comicsCharacter) --> Ballistic
            elif entity_string.endswith(')'):
                left_idx = entity_string.find('(')

                entity_string = entity_string[:left_idx - 1]

                delex_text = delex_text.replace(entity_string,
                                ' ' + entity.ID + ' ')
                matchFound = True

            # if search succeeded, go to next entity, otherwise keep searching
            if matchFound or not advanced:
                continue

            # Non-trivial text matching if
            # 4. try date handling

            # 5. try abbreviations handling

            # 6. try advanced string matching
            delex_text = text_utils.tokenize_and_concat(delex_text)
            best_match = text_utils.find_best_match(entity_string, delex_text)

            if best_match:
                print('\nBEFORE:', best_match, '§' , entity.lex_form, '§', delex_text)
                delex_text = delex_text.replace(best_match,
                                ' ' + entity.ID + ' ')

                print('AFTER:', best_match, '§' , entity.lex_form, '§', delex_text)
                print('TEXT:', self.sentence)
                matchFound = True

            if not matchFound:
                no_match_list.append((entity_string, self.sentence))

        return delex_text, no_match_list


    def get_entityGraph(self):
        """
        Return a dict of entities and thier outgoing edges.
        """
        raise NotImplementedError("To be implemented.")

    def linearize_graph(self, structured=False, incoming_edges=False):
        """
        Generate a linear sequence representing the graph from the triple set
        (flat sequence) or from the entity graphs (structured sequence).
        """

        if not structured:
            seq = ''

            # to generate a flat sequence, linearize rdf_triples
            for triple in self.rdf_triples:
                # extract nodes (entities) and edges (properties)
                subj = triple.subject
                obj = triple.object
                prop = triple.property

                seq = ' '.join(
                                [
                                    seq,
                                    self.entities[subj].lex_form,
                                    self.entities[subj].stype,
                                    self.properties[prop].lex_form,
                                    self.entities[obj].lex_form,
                                    self.entities[obj].stype,
                                ]
                            )
        else:
            # to generate a structured sequence, linearize entity graphs
            if incoming_edges:
                entityGraph = self.obj2subj
            else:
                entityGraph = self.subj2obj

            seq = '¹('

            for (attr, val) in entityGraph.items():
                seq = ' '.join([seq, '²('])
                seq = ' '.join(
                                [
                                    seq,
                                    self.entities[attr].lex_form,
                                    self.entities[attr].stype
                                ]
                           )

                for prop, obj_list in val:
                    seq = ' '.join([seq, '³(', self.properties[prop].lex_form])

                    for obj in obj_list:
                        seq = ' '.join(
                                        [
                                            seq,
                                            '^(',
                                            self.entities[obj].lex_form,
                                            self.entities[obj].stype,
                                            ')^'
                                        ]
                                    )
                    seq = ' '.join([seq, ')³'])
                seq = ' '.join([seq,  ')²'])
            seq = ' '.join([seq, ')¹'])

        return seq.lstrip()


def test():
    xml_str = """<triples>
                    <otriple>Donald Trump | birthPlace | USA</otriple>
                    <otriple>USA | leaderName | Donald Trump</otriple>
                    <otriple>USA | capital | Washington DC</otriple>
                    <otriple>Donald Trump | spouse | Melania Knauss</otriple>
                    <otriple>Melania Knauss | nationality | Slovenia</otriple>
                    <otriple>Melania Knauss | nationality | USA</otriple>
                </triples>"""


    triple_set = et.fromstring(xml_str)

    s = """Donald Trump was born in the United States of Amercia,
        the country where he later became the president . The captial of the US
        is Washington DC . Donald Trump 's wife , Melania Knauss , has two
        nationalities ; American and Slovenian .""".replace('\n', '')

    t = rdf_utils.Tripleset()
    t.fill_tripleset(triple_set)

    test_case = EntityGraph(t, s)

    print('Properties: ', [*test_case.properties])
    print('Entities: ', [*test_case.entities])
    print('subj2obj Graph: ', test_case.subj2obj)
    print('obj2subj Graph: ', test_case.obj2subj)
    print('Linearization: ', test_case.linearize_graph())
    print('Strucutred [1]:',
        test_case.linearize_graph(structured=True))
    print('Strucutred [2]:',
        test_case.linearize_graph(structured=True, incoming_edges=True))

    delex, no_match_list = test_case.delexicalize_text()
    print('Lexicalisation:', delex)

    assert test_case.entities.keys() == \
        {'Donald Trump', 'USA', 'Washington DC', 'Melania Knauss', \
            'Slovenia', 'USA'}, \
        "Test case failed! Entities do not match."

    assert test_case.properties.keys() == \
        {'leaderName', 'birthPlace', 'capital', 'spouse', 'nationality'}, \
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
            ('nationality', ['Slovenia', 'USA'])
            ]
        }, "Test case failed! entityGraph does not match."

    print('\nTesting SUCCESSFUL!')

def main():
    test()

if __name__ == '__main__':
    main()
