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
    Given a sentence (string), return indices of the named entities (list).
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
    for entity in named_entities:
        pass

    return named_entities


def main():
    text = """While in France, Christine Lagarde Johnson discussed short-term
            stimulus efforts in a recent interview with the Wall
            Street Journal on August 1st 2017."""

    E = extract_named_entities(text)

    print(E)

if __name__ == '__main__':
    main()
