#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# transfer bed file to matrix csv file

Usage:
    run_gistic.py call --cnv_fn=IN_FILE [--out_dir=DIR] [--assembly=STR] 
    run_gistic.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --cnv_fn=IN_FILE    Path of cnv csv file.
    --out_dir=DIR       Path of out directory. [default: ./gistic]
    --assembly=STR      The assembly version of the sequence included as part of the reference. [default: hg38]
"""
import numpy as np
import pandas as pd
import docopt
import os 
import subprocess

from biotool import genome
from utils import phylogenetic as phylo
from utils import io


def prepare_gistic_input(seg_fn, marker_fn, cnv_fn, assembly):
    df = io.read_cnv_fn(cnv_fn, 'cell_id')
    m = df.to_numpy()

    current_dir, _ = os.path.split(os.path.realpath(__file__))
    snp6_marker_fn = os.path.join(current_dir, 'utils/db/gistic', '{}_snp_6_markersfile.txt'.format(assembly))

    with open(seg_fn, 'w') as seg_f, open(marker_fn, 'w') as marker_f:
        snp_i = 0
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                cn = m[i, j]
                cell_id =  df.index[i]
                bin = df.columns[j]
                chrom = bin.split(':')[0].replace('chr','')
                start, end = bin.split(':')[1].split('-')
                data = [cell_id, chrom, start, end, 10, cn]
                seg_f.write('\t'.join(map(str, data)) + '\n')

                marker_f.write('SNP_seg_{}\t{}\t{}\n'.format(snp_i, chrom, start))
                snp_i += 1
                marker_f.write('SNP_seg_{}\t{}\t{}\n'.format(snp_i, chrom, end))
                snp_i += 1

        marker_data = open(snp6_marker_fn, 'r').read()
        marker_f.write(marker_data)

def run_gistic(out_dir, seg_fn, marker_fn, assembly):
    current_dir, _ = os.path.split(os.path.realpath(__file__))
    refgene_fn = os.path.join(current_dir, 'utils/db/gistic', '{}.refgene.mat'.format(assembly))

    cmd = '''
    export LD_LIBRARY_PATH=/home/wangmengyao/packages/gistic/MATLAB_Compiler_Runtime/v83/runtime/glnxa64:/home/wangmengyao/packages/gistic/MATLAB_Compiler_Runtime/v83/bin/glnxa64:/home/wangmengyao/packages/gistic/MATLAB_Compiler_Runtime/v83/sys/os/glnxa64:$LD_LIBRARY_PATH
    export XAPPLRESDIR=/home/wangmengyao/packages/gistic/MATLAB_Compiler_Runtime/v83/X11/app-defaults:$XAPPLRESDIR
    /home/wangmengyao/packages/gistic/gp_gistic2_from_seg \
    -b {} -mk {} -seg {} -refgene {} \
    -genegistic 1 -smallmem 1 -broad 1 -brlen 0.5 -conf 0.95 -armpeel 1 -savegene 1 -gcm extreme -maxseg 10000 -v 30 -rx 0 -saveseg 1 -savedata 1 -genepattern 0
    '''.format(out_dir, marker_fn, seg_fn, refgene_fn)

    log_fn = os.path.join(out_dir, 'runtime.log')
    with open(log_fn, 'w') as f:
        proc = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)


def run_call(cnv_fn=None, out_dir=None, assembly='hg38',
             **args):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    seg_fn = os.path.join(out_dir, 'gistic_seg.txt')
    marker_fn = os.path.join(out_dir, 'gistic_marker.txt')
    prepare_gistic_input(seg_fn, marker_fn, cnv_fn, assembly)
    run_gistic(out_dir, seg_fn, marker_fn, assembly)
           

def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
