import requests
import os

GC_URL="https://www.hiv.lanl.gov/cgi-bin/GENE_CUTTER/simpleGC"

input_file="data/seqs/seqs_psc.fasta"
output_dir="data/seqs/Gene_Cutter"
regions_to_align = ['Gag', 'Pol', 'Env']

if not os.path.exists(input_file):
    print(f"No input file. {input_file}")
    exit()

def split_na_aa(text, region, aa_or_na):
    init_seq = f">HXB2_{region}"
    second_index = text.find(init_seq, text.find(init_seq) + 1)
    if aa_or_na == 'na':
        return text[:second_index]
    else:
        return text[second_index:]

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
    region_na = split_na_aa(res.text, region, 'na')
    with open(f'{output_dir}/{region}.aa.fasta', 'w') as out:
        out.write(region_na)
