"""
A module for FactsGraph! It is fun ;-)
"""

from benchmark_reader import Tripleset
from text_utils import *
import xml.etree.ElementTree as et


class FactsGraph():
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

        # a dict to link entities in the graph instance (subj --> (prop, obj))
        # this data structure will facilitate generating structured sequences
        self.entityGraph = self._contruct_graph()

        # find semantic type for each entity in the graph
        # a dict to map between entites and their semantic types
        #self.entity2type = self._get_semantic_types()


    def _contruct_graph(self):
        """
        Build the graph. Populate entity2id, properties and entityGraph dicts.
        """
        eGraph = {}
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

            # populate the entityGraph dict with (prop, obj) tuples
            # flag var to check if the property already added to a node
            FOUND = False

            if subj not in eGraph:
                eGraph[subj] = [(prop, [obj])]
             # if subj entity already seen in the graph
            else:
                # we need to do something smart now
                # loop through all already added (prob, [obj]) tuples
                for i, (p, o) in enumerate(eGraph[subj]):
                    # if the prop already exists, append to the list of object
                    if p == prop:
                        FOUND = True
                        eGraph[subj][i][1].append(obj)
                        break
                    # else, try the next (prob, [obj]) tuple
                    else:
                        continue
                # if the search failed, add a new (prop, [obj]) tuple
                if not FOUND:
                    eGraph[subj].append((prop, [obj]))

        return eGraph


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


    def linearize_graph(self, structured=False):
        """
        Linearize the triple set.
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
                                    subj,
                                    prop,
                                    'ENTITY-' + str(self.entity2id[obj]),
                                    obj
                                ]
                            )

        else:
            # if we want to generate structured sequence, work on the entityGrpah
            seq = '{{'

            for attr, value in self.entityGraph.items():
                seq = ' '.join([seq, '{'])
                seq = ' '.join([seq, 'ENTITY-' + str(self.entity2id[attr]), attr])

                for prob, obj_list in value:
                    seq = ' '.join([seq, '[', prob])

                    for obj in obj_list:
                        seq = ' '.join(
                                        [
                                            seq,
                                            '(',
                                            'ENTITY-'+ str(self.entity2id[obj]),
                                            obj,
                                            ')'
                                        ]
                                        )
                    seq = ' '.join([seq, ']'])
                seq = ' '.join([seq,  '}'])

            seq = ' '.join([seq, '}}'])

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

    t = Tripleset()
    t.fill_tripleset(triple_set)

    test_case = FactsGraph(t, s)

    print('Properties: ', test_case.properties)
    print('Entities: ', test_case.entity2id)
    print('Graph: ', test_case.entityGraph)
    print('Linearization: ', test_case.linearize_graph())
    print('Strucutred:', test_case.linearize_graph(structured=True))

    assert test_case.entity2id.keys() == \
        {'Donald Trump', 'USA', 'Washington DC', 'Melania Knauss', \
            'Slovenia', 'USA'}, \
        "Test case failed! Entities do not match."

    assert test_case.properties == \
        {'leaderName', 'birthPlace', 'capital', 'spouse', 'nationality'}, \
        "Test case failed! Properties do not match."

    assert test_case.entityGraph == \
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

    print('Properties: ', test_case.properties)
    print('Entities: ', test_case.entity2id)
    print('Graph: ', test_case.entityGraph)
    print('Linearization: ', test_case.linearize_graph())

    print('\nTesting SUCCESSFUL!')

def main():
    test()

    triple_set = (
        "Donald Trump | birthPlace | USA",
        "USA | leaderName | Donald Trump",
        "USA | capital | Washington DC",
        "Donald Trump | spouse | Melania Knauss",
        "Melania Knauss | nationality | Slovenia",
        "Melania Knauss | nationality | USA"
        )


if __name__ == '__main__':
    main()
