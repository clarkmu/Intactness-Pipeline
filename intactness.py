"""
This script parallelizes intactness pipeline by splitting sequences
    from input file and running each sequence in parallel.
"""

from Bio.SeqIO import parse as SeqIO_parse

from intactness.__main__ import run_pipeline
from os import path, unlink, makedirs
from multiprocessing.pool import Pool

from intactness.execution_time import ExecutionTime
from intactness.args_parse import gather_args

# cli args
args = gather_args()
seq_in = args['seq_in']
num_threads = args['num_threads']

seq_path = path.dirname(path.abspath(seq_in))

execution_time = ExecutionTime(seq_path)

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

def try_run_pipeline(child_seq_in):
    try:
        run_pipeline(child_seq_in)
    except Exception as e:
        # seq_in = id/main/sample/seqs.fasta
        # print(f'Error running pipeline for {seq_in.rpartition('/')[-2]}: {e}')
        main_dir = path.dirname(seq_in)
        with open(f'{main_dir}/failed_runs.log', 'a+') as f:
            sample = child_seq_in.split('/')[-2]
            f.write(f'Error running pipeline for {sample}. Please see error.log for details.')

# Pool + run all sequences
    # pool.map runs like - each run_pipeline(seq_in)
        #note, multiple running Muscle jobs will stall out a non-clustered CPU
pool = Pool(processes=int(num_threads))
results = pool.map(try_run_pipeline, sequence_inputs)

# merge seq_path/sequence/summary.csv results to seq_in/summary.csv
header="Contig ID,Sample ID,Multi-Contig Sample?,Multi-HIV Sample?,Contig Length,Aligned Length,Aligned coverage of Contig,Ref Seq ID,Aligned Start at Ref,Ref Strand,Is HIV?,Primer,Primer Seq,Large Deletion?,Internal Inversion?,Hypermut?,Hypermut pval,PSC?,gag,pol,env,5' Defect,5' Gaps,5' Inserts,Gag Start Codon Missing?,Gag Start Seq,Final Call,Comments,Contig Sequence"
sample_summaries=[]
summary_errors=[]
for input_seq in sequence_inputs:
    input_path = path.dirname(path.abspath(input_seq))
    summary_file = f'{input_path}/intactness/summary.csv'
    if path.isfile(summary_file):
        with open(summary_file, 'r') as f:
            summary = f.read().split('\n')[1]
            sample_summaries.append(summary)
    else:
        seq = input_path.rpartition('/')[-1]
        no_gaps = f'{input_path}/no_gaps.txt'
        no_seqs_found = f'{input_path}/no_seqs_found.txt'
        if path.isfile(no_gaps):
            # with open(no_gaps, 'r') as f:
            summary_errors.append(f'No gapped position found: {seq}')
        elif path.isfile(no_seqs_found):
            # with open(no_seqs_found, 'r') as f:
            summary_errors.append(f'No sequences found: {seq}')
        else:
            summary_errors.append(f'No summary file found: {seq}')

summary_output = [header]

if len(summary_errors) > 0:
    summary_output += [''] + summary_errors + ['']

summary_output += sample_summaries

with open(f'{seq_path}/summary.csv', 'w') as f:
    f.write('\n'.join(summary_output))

execution_time.finish()

with open(f'{seq_path}/.complete', 'w') as f:
    f.write('')