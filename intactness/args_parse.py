from argparse import ArgumentParser
from os import path

def gather_args():
    parser = ArgumentParser()
    parser.add_argument("-in", "--input", help="Location to input sequences.fasta file. Required.")
    args = parser.parse_args()
    seq_in = args.input
    if not seq_in:
        print('Input missing. Use the -in flag to specify input sequence file location.')
        exit()
    if not path.isfile(seq_in):
        print('-in file does not exist.')
        exit()

    return {
        "seq_in": seq_in
    }
