#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    svOncoprint.py call --sv_gene_fns=IN_FILE --sv_fns=IN_FILE [--sample_fn=IN_FILE] [--out_dir=STR] [--target_gene_fn=IN_FILE]
    svOncoprint.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --sv_gene_fns=IN_FILE       Path of barcode group file.
    --sv_fns=IN_FILE            Path of barcode group file.
    --sample_fn=IN_FILE         Sample file for rename.
"""
import docopt
import numpy as np
import json
import pandas as pd
import collections
import os
import csv 

from biotool import genome
from biotool import gene 

from utils import phylogenetic as phylo
from utils import io
from utils import annotation as anno
import spacelineage

from SVAS.scripts import sv
from SVAS.scripts.compsv import complexsv 


def read_indel_sv_fns(sv_gene_fns, sample_map):
    sv_gene_fns = sv_gene_fns.split(',')
    res_list = [] 
    for sv_gene_fn in sv_gene_fns:
        for row in csv.DictReader(open(sv_gene_fn, 'r')):
            if sample_map:
                if row['Sample'] not in sample_map:
                    continue 
                sample = sample_map[row['Sample']] 
            else:
                sample = row['Sample']
            type = {'INS': 'Small Insertion', 'DEL': 'Small Deletion', 'BND': 'SV'}[row['SV type']]
            for tmp in row['INFO'].split(';'):
                subclone, count = tmp.split('=')
                key = sample + '_' + subclone
                res_list.append([key, row['ID'], row['Gene name'], type])
    return res_list

def read_csv_fns(sv_fns, sample_map):
    sv_fns = sv_fns.split(',')
    res_list = [] 
    for sv_fn in sv_fns:
        for row in csv.DictReader(open(sv_fn, 'r'), delimiter='\t'):
            if sample_map:
                if row['sample'] not in sample_map:
                    continue 
                sample = sample_map[row['sample']] 
            else:
                sample = row['sample']
            type = row['type'].replace('BND:', '')
            for gene in row['genes'].split(','):
                for tmp in row['clone'].split(','):
                    if not tmp:   # debug
                        continue
                    subclone, count = tmp.split('=')
                    key = sample + '_' + subclone
                    id = row['chrom_5p'] + '_' + row['bkpos_5p'] + '_' + row['chrom_3p'] + '_' + row['bkpos_3p']
                    if row['group'].startswith('group'):
                        res_list.append([key, id, gene, 'CSV'])
                    elif row['group'].startswith('chromo'):
                        res_list.append([key, id, gene, 'Chromothripsis'])
                    else: 
                        res_list.append([key, id, gene, type])
                    # single might be missing
    return res_list

def run_call(sv_gene_fns=None, target_gene_fn=None, sv_fns=None, out_dir=None, sample_fn=None, **args):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if sample_fn:
        df = pd.read_csv(sample_fn)[['Sample', 'sample']]
        df = df.set_index('sample')
        sample_map = df.to_dict()['Sample']
    else:
        sample_map = None

    gene_list = gene.read_gene_list(target_gene_fn)

    indel_list = read_indel_sv_fns(sv_gene_fns, sample_map)
    sv_list = read_csv_fns(sv_fns, sample_map)
    res_list = indel_list + sv_list
    total_df = pd.DataFrame(res_list, columns = ['SampleID', 'ID', 'gene', 'type']).drop_duplicates()
    total_df[['Sample', 'Subclone']] = total_df.SampleID.str.split('_', expand=True)
    df = total_df.groupby(by=['Sample', 'type', 'gene', 'ID']).agg({'Subclone': set}).reset_index()
    df.Subclone = df.Subclone.apply(lambda x: ';'.join(sorted(list(x))))
    df.to_csv(os.path.join(out_dir, 'sv_subclone.csv'))

    # sv gene count
    df = total_df[['SampleID', 'ID', 'gene', 'type']].drop_duplicates()
    df = df[df.gene != '']
    df = df[['SampleID', 'gene', 'type']].drop_duplicates()
    sv_gene_count_df = df.groupby(by=['SampleID', 'type'])['gene'].count().reset_index(name='gene_count')
    sv_gene_count_df.to_csv(os.path.join(out_dir, 'sv_gene_count.csv'))

    # sv count
    df = total_df[['SampleID', 'ID', 'type']].drop_duplicates()
    sv_count_df = df.groupby(by=['SampleID', 'type'])['ID'].count().reset_index(name='count')
    sv_count_df.to_csv(os.path.join(out_dir, 'sv_count.csv'))

    # oncoprint
    if gene_list:
        df = total_df[total_df.gene.isin(gene_list)]
    else:
        df = total_df
    df = df[df.type.isin(['Small Insertion', 'Small Deletion', 'SV', 'CSV', 'Chromothripsis'])]
    df.type[df.type == 'Small Insertion'] = 'InDel' 
    df.type[df.type == 'Small Deletion'] = 'InDel' 
    df = df[['SampleID', 'gene', 'type']].drop_duplicates()
    df.gene = 'g_' + df.gene
    df = df.groupby(by=['SampleID', 'gene'])['type'].apply(list).reset_index(name='type')
    df = df.pivot(index="SampleID", columns="gene", values="type").fillna('-')
    df = df.applymap(';'.join)
    df.to_csv(os.path.join(out_dir, 'oncoprint.csv'))

def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
