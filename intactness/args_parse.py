from argparse import ArgumentParser
from os import path

def gather_args():
    parser = ArgumentParser()
    parser.add_argument("-in", "--input", help="Location to input sequences.fasta file. Required.")
    parser.add_argument("-email", "--email", help="Email to receive results. Optional if running on your own server.")
    parser.add_argument("-env", "--conda-env", help="Set conda environment to use. Optional.")
    parser.add_argument("-n", "--num-threads", help="Number of threads to use. Optional. Default")
    args = parser.parse_args()
    seq_in = args.input
    if not seq_in:
        print('Input missing. Use the -in flag to specify input sequence file location.')
        exit()
    if not path.isfile(seq_in):
        print('-in file does not exist.')
        exit()

    return {
        "seq_in": seq_in,
        "email": args.email,
        "conda_env": args.conda_env,
        "num_threads": args.num_threads if args.num_threads else 1
    }
