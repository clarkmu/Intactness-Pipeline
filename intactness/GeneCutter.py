# coding: utf-8
import re
import logging

import os

import requests

from collections import defaultdict

# pylint: disable=C0103
# Invalid constant name
logger = logging.getLogger('pipe.GeneCutter')

GC_URL="https://www.hiv.lanl.gov/cgi-bin/Gene_Cutter/simpleGC"

def submit_GC():
    """
    Submit aligned seqs to Gene Cutter and start the job

    """

    input_file="data/seqs/seqs_psc.fasta"
    output_dir="data/seqs/Gene_Cutter"

    # UPDATE JAN 2024
    # Use SimpleGC API instead of MechanicalSoup to simulate form submission

    # this cannot be reused
    # files={'seq_upload': open(input_file, 'rb')}
    data={'insert_ref': 'Yes'}

    # curl --form region="Gag" --form translate="No" --form "seq_upload=@data/seqs/seqs_psc.fasta" --form "insert_ref=Yes" https://www.hiv.lanl.gov/cgi-bin/GENE_CUTTER/simpleGC
    res = requests.post(GC_URL, data=data, files={'seq_upload': open(input_file, 'rb')})

    os.makedirs(output_dir, exist_ok=True)

    with open(f'{output_dir}/ALL.AA.PRINT', 'w') as out:
        out.write(res.text)

    data['return_format']="fasta"
    for region in ['Gag', 'Pol', 'Env']:
        data['region'] = region
        res = requests.post(GC_URL, data=data, files={'seq_upload': open(input_file, 'rb')})
        with open(f'{output_dir}/{region}.aa.fasta', 'w') as out:
            out.write(res.text)

def process_GC():
    # Parse results
    results = defaultdict(dict)

    gene_set = set(['Gag', 'Pol', 'Env'])
    with open('data/seqs/Gene_Cutter/ALL.AA.PRINT') as fn:
        line = fn.readline()
        while line:
            if line.startswith('---------- List of Stop Codons Within Sequences'):
                gene = re.search('^.*\((.*)\).*$', line).group(1)
                if gene in gene_set:
                    line = fn.readline()

                    while True:
                        if line == '\n':
                            line = fn.readline()
                        elif line.startswith('----'):
                            break
                        else:
                            line = line.strip()
                            seq_id, _, pos = line.split(' ')
                            results[gene].setdefault(seq_id, set()).add((int(pos), 'SC', ''))
                            line = fn.readline()
                else:
                    line = fn.readline()

            elif line.startswith('---------- List of Incomplete Codons'):
                gene = re.search('^.*\((.*)\).*$', line).group(1)
                if gene in gene_set:
                    line = fn.readline()

                    while True:
                        if line == '\n':
                            line = fn.readline()
                        elif line.startswith('----'):
                            break
                        else:
                            line = line.strip()
                            seq_id, _, pos, ic_type = line.split(' ')
                            results[gene].setdefault(seq_id, set()).add((int(pos), 'IC', ic_type))
                            line = fn.readline()
                else:
                    line = fn.readline()
            else:
                line = fn.readline()

    if (len(results) == 0):
        with open('data/seqs/summary_psc.tsv', 'w') as fn:
            print('Contig\tRef\tType\tPSC', file=fn)
    else:
        final_results = defaultdict(dict)
        for gene, contigs in results.items():
            for contig, events in contigs.items():
                events = sorted(events)
                idx_used = []
                for idx, event in enumerate(events):
                    if idx <= 1:
                        final_results.setdefault(gene, {}).setdefault(contig, {}).setdefault(event[1], []).append((event[0], event[2]))
                    elif events[idx][1] == 'IC' and \
                        events[idx - 1][1] == 'SC' and \
                        events[idx - 2][1] == 'IC' and \
                        events[idx-1][0] - events[idx-2][0] < 100 and \
                        events[idx][0]   - events[idx-1][0] < 100:
                        del final_results[gene][contig]['IC'][-1]
                        del final_results[gene][contig]['SC'][-1]
                    else:
                        final_results.setdefault(gene, {}).setdefault(contig, {}).setdefault(event[1], []).append((event[0], event[2]))

        with open('data/seqs/summary_psc.tsv', 'w') as fn:
            print('Contig\tRef\tType\tPSC', file=fn)
            # Remove beginning and ending
            for gene, contigs in final_results.items():
                for contig, event_types in contigs.items():
                    for event_type, events in event_types.items():
                        events = [event for event in events if event[0] != 1]
                        if (event_type == 'SC'):
                            events = ";".join(str(event[0]) for event in events)
                        else:
                            events = ";".join(str(event[0])+ ":" + event[1] for event in events)
                        if events == '':
                            continue
                        print("{}\t{}\t{}({})\tYes".format(contig, gene, event_type, events), file=fn)


if __name__ == '__main__':
    submit_GC()
    process_GC()
