# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 00:29:42 2017

@author: Ce Gao
@author: Rong Chen
"""
# pylint: disable=C0103
# Disable module level constant name checking

from logging import getLogger, INFO
from os import path
from time import time

from intactness.args_parse import gather_args

# Local module
from .view import View
from .sequence import Sequences
from .configs import configs
from .blast import blast
from .muscle import muscle
from .gag_codon import gag_codon
from .primer import primer
from .hypermut import hypermut
from .psc import psc
from .defect import defect
from .summary import summary

logger = getLogger('pipe')
logger.setLevel(INFO)

args = gather_args()

def run_pipeline(seq_in):
    start_time = time()
    mod_path = path.dirname(path.abspath(__file__))
    cfg = configs(path.join(mod_path, 'default.cfg'), seq_in)
    seqs = Sequences(cfg['Query'], cfg['Reference'])
    primer(cfg['Primer'], seqs)
    blast(cfg['BLAST'], seqs)
    View(cfg['View']).run()
    muscle(cfg['MSA'])
    gag_codon(cfg['Codon'], seqs)
    hypermut(cfg['Hypermut'], seqs)
    psc(cfg['PSC'], seqs, seq_in)
    defect(cfg['Defect'], seqs)
    summary(cfg['Summary'], seqs)
    with open(f"{seq_in[:seq_in.rindex('/')]}/execution_time.txt", 'w') as f:
        f.write(f'{(time() - start_time)/60} minutes')

if __name__ == '__main__':
    run_pipeline(args['seq_in'])