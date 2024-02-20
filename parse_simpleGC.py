import requests
import os

GC_URL="https://www.hiv.lanl.gov/cgi-bin/GENE_CUTTER/simpleGC"

input_file="data/seqs/seqs_psc.fasta"
output_dir="data/seqs/Gene_Cutter"
regions_to_align = ['Gag', 'Pol', 'Env']

if not os.path.exists(input_file):
    print(f"No input file. {input_file}")
    exit()

# this cannot be reused
# files={'seq_upload': open(input_file, 'rb')}
data={'insert_ref': 'Yes'}

os.makedirs(output_dir, exist_ok=True)

res=requests.post(GC_URL, files={'seq_upload': open(input_file, 'rb')}, data=data)

with open(f"{output_dir}/ALL.AA.PRINT", 'w') as out:
    out.write(res.text)

data['return_format']="fasta"
for region in regions_to_align:
    data['region'] = region
    res=requests.post(GC_URL, files={'seq_upload': open(input_file, 'rb')}, data=data)
    with open(f'{output_dir}/{region}.aa.fasta', 'w') as out:
        out.write(res.text)
