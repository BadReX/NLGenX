"""
A module to process input data and generate dataset for training and inference.
"""

import IO_utils
import argparse
import EntityGraph

def generate():
    # get a directory from user input
    DISCR = 'Generate dataset from XML files of RDF to Text Entries.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to data.', required=True)
    parser.add_argument('-input_mode', help='Input mode: linear or structured.',
                    choices=['linear', 'structured'], default = 'linear', nargs = '?')

    parser.add_argument('-src', type=str, help='Path to output file for src.',
                    required=True)
    parser.add_argument('-tgt', type=str, help='Path to output file for tgt.',
                    required=True)

    args = parser.parse_args()

    instances = IO_utils.generate_instances(args.path)

    for (size, ins) in instances.items():
        for i in ins:
            G = EntityGraph.EntityGraph(i.modifiedtripleset, i.Lexicalisation.lex)

            with open(args.src, 'a+') as srcFile:
                if args.input_mode == 'linear':
                    srcFile.write(G.linearize_graph() + '\n')
                else:
                    srcFile.write(G.linearize_graph(structured=True) + '\n')

            with open(args.tgt, 'a+') as tgtFile:
                tgtFile.write(G.sentence  + '\n')


def main():
    generate()

if __name__ == '__main__':
    main()
