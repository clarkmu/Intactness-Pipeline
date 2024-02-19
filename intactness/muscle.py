#!/usr/bin/env python3
"""
multiple sequence alignment using muscle
"""

from .utils import run_cmd


def muscle(configs):
    """Multiple sequence alignment using muscle
    """

    file_i = configs['file_seq']
    file_o = configs['file_aln']
    # maxiters = configs['maxiters']

    cmd = ['muscle', '-super5', file_i, '-output', file_o]
    run_cmd(cmd)
