#!/usr/bin/env python
"""
Basic script to create an empty python package containing one module
"""
from benchmark_reader import *
from nltk.chunk import conlltags2tree

class FactsGraph():
    """
    A class to represent instances of RDF to Text instances for natural
    language generation from structed data input (e.g. KB RDF triples).
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

        # a set of entities in the graph instance
        self.entities = set()

        # a set of properties in the graph instance
        self.properties = set()

        # a dict to link entities in the graph instance (subj --> (prop, obj))
        self.entityGraph = {}

        # call contruct_graph() method to build the graph from the RDF triples
        self._contruct_graph()

    def _contruct_graph(self):
        """
        Build the graph.
        """
        # loop through each triple
        for triple in self.rdf_triples:
            # extract nodes (entities) and edges (properties)
            subj = triple.subject
            obj = triple.object
            prop = triple.property

            # update dicts
            self.entities.update((subj, obj))
            self.properties.add(prop)

            # initialize the entityGraph dict with (prop, obj) tuples
            if subj not in self.entityGraph.keys():
                self.entityGraph[subj] = [(prop, obj)]
            else: # if subj entity already seen in the graph
                self.entityGraph[subj].append((prop, obj))


st = StanfordNERTagger(
    '/home/badr/StanfordNLP/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
    '/home/badr/StanfordNLP/stanford-ner/stanford-ner.jar',
    encoding='utf-8')

def test():
    triple_set = (
        "Donald Trump | birthPlace | USA",
        "USA | leaderName | Donald Trump",
        "USA | capital | Washington DC",
        "Donald Trump | spouse | Melania Knauss",
        "Melania Knauss | nationality | Slovenia",
        "Melania Knauss | nationality | USA"
        )

    s = "Trump was born in the united states of Amercia, \
            which captial is Washington DC."

    t = Tripleset(triple_set)
    test_case = FactsGraph(t, s)

    print('Properties: ', test_case.properties)
    print('Entities: ', test_case.entities)
    print('Graph: ', test_case.entityGraph)

    assert test_case.entities == \
        {'Donald Trump', 'USA', 'Washington DC', 'Melania Knauss', \
            'Slovenia', 'USA'}, \
        "Test case failed! Entities do not match."

    assert test_case.properties == \
        {'leaderName', 'birthPlace', 'capital', 'spouse', 'nationality'}, \
        "Test case failed! Properties do not match."

    assert test_case.entityGraph == \
        {'Donald Trump': [ \
            ('birthPlace', 'USA'),
            ('spouse', 'Melania Knauss')
            ],
        'USA': [
            ('leaderName', 'Donald Trump'),
            ('capital', 'Washington DC')
            ],
        'Melania Knauss': [
            ('nationality', 'Slovenia'),
            ('nationality', 'USA')
            ]
        }, "Test case failed! entityGraph does not match."

    print('Properties: ', test_case.properties)
    print('Entities: ', test_case.entities)
    print('Graph: ', test_case.entityGraph)

    print('\nTesting SUCCESSFUL!')

    # if sentence is given, extract named entites with NLTK NER
    if test_case.sentence:
        self.name_entities = extract_named_entities(test_case.sentence)


def main():
    """Basic command line bootstrap for the BasicModule Skeleton"""
    #BasicModule.cmd()
    test()


if __name__ == '__main__':
    main()
