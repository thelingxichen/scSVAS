#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    recurrent_region.py cnv --cnv_fns=IN_FILES --samples=STR [--target_gene_fn=IN_FILE] [--out_prefix=STR] [--ref=STR]
    recurrent_region.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --cnv_fns=IN_FILES          List of SCYN format cnv file path, seperated by comma ','
    --samples=STR               List of sample names, seperated by comma ','
    --target_gene_fn=IN_FILE    Path of SCYN format meta file.
    --out_prefix=STR            Path of out file prefix, [default: ./recurrent]
    --ref=STR                   Reference version, [default: hg38]
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
import json

from utils import phylogenetic as phylo
from utils import io
from utils import embedding
from utils import annotation as anno

######## annotate bin changes ############

def annotate_shifts(t, cnv_df, shift=0.5, target_gene_fn=None, ref='hg38'):

    for link in t.links:
        p_cnv = link.source.cnv
        c_cnv = link.target.cnv

        shifts = np.array(c_cnv) - np.array(p_cnv)
        amp_index = sum(np.argwhere(shifts > shift).tolist(),[])
        loss_index = sum(np.argwhere(shifts < -shift).tolist(),[])
        amp_bins = cnv_df.iloc[:,amp_index].columns.tolist()
        loss_bins = cnv_df.iloc[:,loss_index].columns.tolist()

        amp_bins_dict = deal_shift_dict(amp_bins, amp_index, link)
        loss_bins_dict = deal_shift_dict(loss_bins, loss_index, link)

        link.meta = '{} amp, {} loss'.format(len(amp_bins), len(loss_bins))
        # bin: {gene:[], cnv:[p, c, shift]}
        link.shift_bins = {'amp': amp_bins_dict, 'loss': loss_bins_dict}
        call_bedtool_bin2gene(amp_bins, ref, link=link, shift_type='amp', target_gene_fn=target_gene_fn)
        call_bedtool_bin2gene(loss_bins, ref, link=link, shift_type='loss', target_gene_fn=target_gene_fn)


def deal_shift_dict(bins, bin_index, link):
    res = {}
    for bin, index in zip(bins, bin_index):
        p_cnv = link.source.cnv[index]
        c_cnv = link.target.cnv[index]
        res[bin] = {'cnv': [p_cnv, c_cnv, c_cnv-p_cnv]}
    return res


def call_bedtool_bin2gene(bin_list, ref, use_db=True, target_gene_fn=None, **kwargs):
    bin_bed = anno.get_bin_bed(bin_list)
    gene_bed = anno.get_gene_bed(ref, use_db=use_db, target_gene_fn=target_gene_fn)

    prev_bin = None
    hits = []
    for i, hit in enumerate(bin_bed.window(gene_bed).overlap(cols=[2, 3, 5, 6])):
        if i > 5: break
        bin = '{}:{}-{}'.format(hit[0], hit[1], hit[2])
        if prev_bin != bin and hits:
            process_bin2gene_hits(bin, hits, **kwargs)
            hits = []
        hits.append(hit)
        prev_bin = bin


def process_bin2gene_hits(bin, hits, link=None, shift_type=None,
                          **kwargs):
    gene_list = [hit[6].split(',')[0] for hit in hits]
    link.shift_bins[shift_type][bin]['gene'] = gene_list


def run_cnv(cnv_fns=None, samples=None, target_gene_fn=None, out_prefix=None, ref='hg38', **args):
    cnv_index_name = 'cell_id'
    samples = samples.split(',')

    cnv_df_list = []
    for sample, cnv_fn in zip(samples, cnv_fns.split(',')):
        cnv_df = io.read_cnv_fn(cnv_fn, cnv_index_name)
        cnv_df.set_index(sample + '_' + cnv_df.index.astype(str))
        cnv_df_list.append(cnv_df)

    df = pd.concat(cnv_df_list)

def get_tree_link_tsv(label, t):
    res = ''
    for link in t.links:
        for bin, bin_dict in link.shift_bins['amp'].items():
            p, c ,s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            if 'gene' not in bin_dict:
                continue
            gene_str = ','.join(bin_dict.get('gene', []))
            r = [label, link.source.name, link.target.name, 'amp', bin, p, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
        for bin, bin_dict in link.shift_bins['loss'].items():
            p, c ,s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            if 'gene' not in bin_dict:
                continue
            gene_str = ','.join(bin_dict.get('gene', []))
            r = [label, link.source.name, link.target.name, 'loss', bin, p, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
    return res



def run(cnv=None, **args):
    if cnv:
        run_cnv(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
