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

from intactness.args_parse import gather_args
from .email_error import send_error

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
from .email_results import send_results
from .execution_time import ExecutionTime
from .utils import run_cmd

logger = getLogger('pipe')
logger.setLevel(INFO)

args = gather_args()

job_dir = path.dirname(path.abspath(args['seq_in']))

def run_pipeline(seq_in, email = "", conda_env=""):
    if conda_env:
        run_cmd(['conda', 'activate', conda_env])

    mod_path = path.dirname(path.abspath(__file__))
    cfg = configs(path.join(mod_path, 'default.cfg'), seq_in)
    execution_time = ExecutionTime(cfg['Main']['path_out'])

    def quit_no_gaps():
        with open(f"{job_dir}/no_gaps.txt", 'w+') as f:
            f.write("No gapped position found given a position on the reference genome. No results will be generated.")
        execution_time.finish()
        return

    seqs = Sequences(cfg['Query'], cfg['Reference'])
    primer(cfg['Primer'], seqs)
    found_seqs = blast(cfg['BLAST'], seqs)

    if found_seqs == False:
        with open(f"{job_dir}/no_seqs_found.txt", 'w+') as f:
            f.write("All sequences were filtered out during Blast. No results will be generated.")
        execution_time.finish()
        return

    View(cfg['View']).run()
    muscle(cfg['MSA'])
    gag_codon(cfg['Codon'], seqs, quit_no_gaps)
    hypermut(cfg['Hypermut'], seqs)
    psc(cfg['PSC'], seqs, seq_in)
    defect(cfg['Defect'], seqs, quit_no_gaps)
    summary(cfg['Summary'], seqs)
    # if email:
    #     send_results(email, cfg['Main']['path_dat'])
    execution_time.finish()

if __name__ == '__main__':
    try:
        run_pipeline(args['seq_in'], args['email'], args['conda_env'])
    except BaseException as e:
        with open(f"{job_dir}/error.log", 'w+') as f:
            f.write("An uncaught error has occurred during processing:\n" + str(e))
        if args['email']:
            send_error(args['email'], str(e))