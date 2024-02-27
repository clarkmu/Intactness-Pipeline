"""
This script parallelizes intactness pipeline by splitting sequences
    from input file and running each sequence in parallel.
"""

from Bio.SeqIO import parse as SeqIO_parse

from intactness.__main__ import run_pipeline
from os import path, unlink, makedirs
from multiprocessing.pool import Pool
from time import time

from intactness.args_parse import gather_args

start_time = time()

# cli args
args = gather_args()
seq_in = args['seq_in']

seq_path = path.dirname(path.abspath(seq_in))

sequence_inputs = []

# split input by sequence and write to files
seqs = SeqIO_parse(seq_in, "fasta")
for seq in seqs:
    new_path=f'{seq_path}/sequences/{seq.id}'
    makedirs(new_path, exist_ok=True)
    new_input=f'{new_path}/seqs.fasta'
    sequence_inputs.append(new_input)
    with open(new_input, 'w') as f:
        f.write(f'>{seq.id}\n{seq.seq}')

# Pool + run all sequences
    # pool.map runs like - each run_pipeline(seq_in)
        #note, multiple running Muscle jobs will stall out a non-clustered CPU
pool = Pool(processes=1)
results = pool.map(run_pipeline, sequence_inputs)

# merge seq_path/sequence/summary.csv results to seq_in/summary.csv
header="Contig ID,Sample ID,Multi-Contig Sample?,Multi-HIV Sample?,Contig Length,Aligned Length,Aligned coverage of Contig,Ref Seq ID,Aligned Start at Ref,Ref Strand,Is HIV?,Primer,Primer Seq,Large Deletion?,Internal Inversion?,Hypermut?,Hypermut pval,PSC?,gag,pol,env,5' Defect,5' Gaps,5' Inserts,Gag Start Codon Missing?,Gag Start Seq,Final Call,Comments,Contig Sequence"
summaries=[]
for input_seq in sequence_inputs:
    input_path = path.dirname(path.abspath(input_seq))
    with open(f'{input_path}/summary.csv', 'r') as f:
        summary = f.read().split('\n')[1]
        summaries.append(summary)

with open(f'{seq_path}/summary.csv', 'w') as f:
    f.write(header + '\n' + '\n'.join(summaries) + '\n')

# unlink(f'{seq_path}/sequences')

with open(f"{seq_path}/execution_time.txt", 'w') as f:
        f.write(f'{(time() - start_time)/60} minutes')