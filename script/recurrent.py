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
from io import StringIO

from utils import phylogenetic as phylo
from utils import io
from biotool import genome
from utils import annotation as anno
import run_gistic



def call_bedtool_bin2gene(amp_bins, del_bins, ref, use_db=True, target_gene_fn=None, **kwargs):
    bin_list = amp_bins.keys() & del_bins.keys()
    bin_bed = anno.get_bin_bed(bin_list)
    gene_bed = anno.get_gene_bed(ref, use_db=use_db, target_gene_fn=target_gene_fn)

    prev_bin = None
    hits = []
    for i, hit in enumerate(bin_bed.window(gene_bed).overlap(cols=[2, 3, 5, 6])):
        bin = '{}:{}-{}'.format(hit[0], hit[1], hit[2])
        if prev_bin != bin and hits:
            process_bin2gene_hits(bin, hits, amp_bins, del_bins, **kwargs)
            hits = []
        hits.append(hit)
        prev_bin = bin


def process_bin2gene_hits(bin, hits, amp_bins, del_bins, cytoband_dict=None,
                          **kwargs):
    gene_list = [hit[6].split(',')[0] for hit in hits]
    cytoband = genome.get_cytoband_from_bin_str(cytoband_dict, bin)
    if bin in amp_bins:
        amp_bins[bin]['gene'] = gene_list
        amp_bins[bin]['cytoband'] = cytoband 
    if bin in del_bins:
        del_bins[bin]['gene'] = gene_list
        del_bins[bin]['cytoband'] = cytoband 


def run_cnv(cnv_fns=None, samples=None, target_gene_fn=None, out_prefix=None, ref='hg38', **args):
    cnv_index_name = 'cell_id'
    samples = samples.split(',')

    cnv_df_list = []
    for sample, cnv_fn in zip(samples, cnv_fns.split(',')):
        cnv_df = io.read_cnv_fn(cnv_fn, cnv_index_name)
        cnv_df.index = sample + '_' + cnv_df.index.astype(str)
        cnv_df_list.append(cnv_df)
        # run_gistic.run_call(cnv_fn=cnv_df, out_dir='./recurrent_{}'.format(sample))

    df = pd.concat(cnv_df_list)
    # run_gistic.run_call(cnv_fn=df, out_dir='./recurrent')
    res, amp_bins, del_bins = detect_recurrent(df)

    ## annotate
    cytoband_dict = genome.read_cytoband(ref)
    call_bedtool_bin2gene(amp_bins, del_bins, ref, target_gene_fn=target_gene_fn, cytoband_dict=cytoband_dict)
    res_dict = {'amp_anno': amp_bins,
           'del_anno': del_bins,
           'samples': res}

    res = json.dumps(res_dict, indent=4)
    json_fn = out_prefix + '.json'
    with open(json_fn, 'w') as f:
        f.write(res)

    ###### output recurrent ########
    evo_fn = out_prefix + '.tsv'
    res = '\t'.join(['sample_group', 'amp/del', 'region', 'cytoband', 'cnv', 'shift', 'gene'])+'\n'
    res += get_recurrent_tsv(res_dict)
    df = pd.read_csv(StringIO(res), sep='\t')
    df = df.sort_values(['region', 'amp/del'])
    print(df)
    df.to_csv(evo_fn, sep='\t', index=False)

def get_recurrent_tsv(res_dict):
    res = ''
    for sample, v in res_dict['samples'].items():
        for bin, bin_dict in v['bin'] ['amp'].items():
            if bin not in res_dict['amp_anno']: 
                continue
            p, c ,s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            gene_str = ','.join(res_dict['amp_anno'][bin].get('gene', []))
            cytoband = res_dict['amp_anno'][bin].get('cytoband', '')
            r = [sample, 'amp', bin, cytoband, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
        for bin, bin_dict in v['bin'] ['loss'].items():
            if bin not in res_dict['del_anno']: 
                continue
            p, c ,s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            gene_str = ','.join(res_dict['del_anno'][bin].get('gene', []))
            cytoband = res_dict['del_anno'][bin].get('cytoband', '')
            r = [sample, 'del', bin, cytoband, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
    return res


def detect_recurrent(df):
    bins = df.columns
    df['sample'] = df.index.str.split('_').str[0]
    df['cluster'] = df.index.str.split('_').str[1]
    res = { key:{'bin':{'amp':{}, 'loss':{}}, 'cnv':df.loc[key, bins].to_dict()}  for key in df.index }
    amp_bins = {} 
    del_bins = {} 
    for i, bin in enumerate(bins):
        if i > 100: break
        bin_df = df[['sample', 'cluster', bin]]
        bin_df['amp'] = bin_df[bin] > 3 
        bin_df['del'] = bin_df[bin] < 1 
        count_df = bin_df.groupby('sample').sum()
        num_samples = count_df.shape[0]
        if (count_df['amp'] == 0).sum() < num_samples - 1:
            tmp = bin_df[bin_df['amp'] == True]
            update_bin_dict(tmp, bin, 'amp', res)
            amp_bins[bin] = {} 

        if (count_df['del'] == 0).sum() < num_samples - 1:
            tmp = bin_df[bin_df['del'] == True]
            update_bin_dict(tmp, bin, 'loss', res)
            del_bins[bin] = {}
    return res, amp_bins, del_bins

def update_bin_dict(df, bin, shift_type, res):
    for key, cn in df[bin].to_dict().items():
        res[key]['bin'][shift_type][bin] = {"cnv": [2, cn, cn - 2]}


def run(cnv=None, **args):
    if cnv:
        run_cnv(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
