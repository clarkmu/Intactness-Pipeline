#!/usr/bin/env python3
"""
multiple sequence alignment using muscle
"""

from os.path import exists, dirname
from os import makedirs
from .utils import run_cmd


def muscle(configs):
    """Multiple sequence alignment using muscle
    """

    file_i = configs['file_seq']
    file_o = configs['file_aln']
    # maxiters = configs['maxiters']

    if not exists(file_i):
        print("Missing Muscle Input")
        exit()

    makedirs(dirname(file_o), exist_ok=True)

    cmd = ['muscle', '-super5', file_i, '-output', file_o]
    run_cmd(cmd)

    if not exists(file_o):
        raise BaseException("Muscle failed")
