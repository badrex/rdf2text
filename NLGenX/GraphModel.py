"""
A module for Entity, Property, and EntityGraph! It is fun ;-)
"""
#from utils import text_utils
from utils import rdf_utils
import xml.etree.ElementTree as et


class EntityClass:
    """ A class to represent an RDF entity. """

    def __init__(self, RDF_entity, semantic_type):
        """
        Instantiate an entity.
        :param RDF_entity: an entity from an RDF triple (dtype: string)
        """
        self.lex_form = self.text_split(RDF_entity)
        self.stype = semantic_type
        self.aliases = self.get_aliases()

    def text_split(self, RDF_entity):
        """Return the text of the entity after split."""
        return ' '.join(RDF_entity.split('_'))

    def get_aliases(self):
        """Return a list of aliases for the entity."""
        return [self.lex_form, self.lex_form.lower()]


# namedtuple for entity instances
# IDEA: structure entity as a dict of entity[lex_form] --> entityObject

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
            raise NotImplementedError("To be implemented.")


class EntityGraph():
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

        # a dict for entities in the graph instance entity --> id
        self.entity2id = {}

        # a set of properties in the graph instance
        self.properties = set()

        # call contruct_graph() method to build the graph from the RDF triples

        # two dicts to link entities in the graph instance (subj --> (prop, obj))
        # and (obj --> (prop, subj))
        # this data structure will facilitate generating structured sequences
        self.subj2obj = {}
        self.obj2subj = {}

        # call method to construct entity graph and populate other dicts
        self._contruct_graph()

        # TODO: maybe move this somewhere else!!!
        # find semantic type for each entity in the graph
        # a dict to map between entites and their semantic types
        #self.entity2type = self._get_semantic_types()

    def _contruct_graph(self):
        """
        Build the graph. Populate entity2id, properties, subj2obj and obj2subj dicts.
        """
        entityID = 0

        # loop through each triple
        for triple in self.rdf_triples:
            # extract nodes (entities) and edges (properties)
            subj = triple.subject
            obj = triple.object
            prop = triple.property

            # update entities dict
            if subj not in self.entity2id:
                entityID += 1
                self.entity2id[subj] = entityID

            if obj not in self.entity2id:
                entityID += 1
                self.entity2id[obj] = entityID

            # add to properties
            self.properties.add(prop)

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


    def _get_semantic_types(use_schema=False):
        """
        For each entity (node) in the graph, find the semantic type.
        """
        raise NotImplementedError("To be implemented.")


    def delexicalize_sentence(self):
        """
        Apply delexicalization on sentence.
        """
        raise NotImplementedError("To be implemented.")


    def get_entityGrpah(self):
        """
        Return a dict of entities and thier outgoing edges.
        """
        raise NotImplementedError("To be implemented.")

    def linearize_graph(self, structured=False, incoming_edges=False):
        """
        Linearize the graph from triple set (flat sequence)
        or from the entityGraph (structured sequence).
        """

        if not structured:
            seq = ''
            for triple in self.rdf_triples:
                # extract nodes (entities) and edges (properties)
                subj = triple.subject
                obj = triple.object
                prop = triple.property

                seq = ' '.join(
                                [
                                    seq,
                                    'ENTITY-' + str(self.entity2id[subj]),
                                    'AGENT', #subj,
                                    prop,
                                    'ENTITY-' + str(self.entity2id[obj]),
                                    'PATIENT', #obj
                                ]
                            )
        else:
            # if we want to generate structured sequence, work on the entityGrpah
            if incoming_edges:
                entityGraph = self.obj2subj
            else:
                entityGraph = self.subj2obj

            seq = '¹('

            for attr, value in entityGraph.items():
                seq = ' '.join([seq, '²('])
                seq = ' '.join([seq, 'ENTITY-' + str(self.entity2id[attr]), 'AGENT']) # attr

                for prob, obj_list in value:
                    seq = ' '.join([seq, '³(', prob])

                    for obj in obj_list:
                        seq = ' '.join(
                                        [
                                            seq,
                                            '^(',
                                            'ENTITY-'+ str(self.entity2id[obj]),
                                            'PATIENT', #obj,
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
        the country whrere he later became the president. The captial of the US
        is Washington DC. Donald Trump's wife, Melania Knauss, has two
        nationalities; American and Slovenian."""

    t = rdf_utils.Tripleset()
    t.fill_tripleset(triple_set)

    test_case = EntityGraph(t, s)

    print('Properties: ', test_case.properties)
    print('Entities: ', test_case.entity2id)
    print('subj2obj Graph: ', test_case.subj2obj)
    print('obj2subj Graph: ', test_case.obj2subj)
    print('Linearization: ', test_case.linearize_graph())
    print('Strucutred [1]:', test_case.linearize_graph(structured=True))
    print('Strucutred [2]:', test_case.linearize_graph(structured=True,
                                                        incoming_edges=True))

    assert test_case.entity2id.keys() == \
        {'Donald Trump', 'USA', 'Washington DC', 'Melania Knauss', \
            'Slovenia', 'USA'}, \
        "Test case failed! Entities do not match."

    assert test_case.properties == \
        {'leaderName', 'birthPlace', 'capital', 'spouse', 'nationality'}, \
        "Test case failed! Properties do not match."

    assert test_case.subj2obj == \
        {'Donald Trump': [ \
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
