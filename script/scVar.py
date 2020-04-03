#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    scVar.py cnv --cnv_fn=IN_FILE [--meta_fn=IN_FILE] [--nwk_fn=IN_FILE] [--target_gene_fn=IN_FILE] [--k=INT] [--out_prefix=STR] [--ref=STR]
    scVar.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --cnv_fn=IN_FILE            Path of SCYN format cnv file.
    --meta_fn=IN_FILE           Path of SCYN format meta file.
    --nwk_fn=IN_FILE            Path of build tree, scVar will build one if not supplied.
    --target_gene_fn=IN_FILE    Path of SCYN format meta file.
    --k=INT                     Number of clusters in the tree at the cut point. [default: 7]
    --out_prefix=STR            Path of out file prefix, [default: ./phylo]
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
        bin = '{}:{}-{}'.format(hit[0], hit[1], hit[2])
        if prev_bin != bin and hits:
            process_bin2gene_hits(prev_bin, hits, **kwargs)
            hits = []
        hits.append(hit)
        prev_bin = bin


def process_bin2gene_hits(bin, hits, link=None, shift_type=None,
                          **kwargs):
    gene_list = [hit[6].split(',')[0] for hit in hits]
    link.shift_bins[shift_type][bin]['gene'] = gene_list
    if 'NOTCH2' in gene_list:
        print(bin)
        print(hits)
        print(gene_list)


def run_cnv(cnv_fn=None, meta_fn=None, nwk_fn=None, target_gene_fn=None, k=None, cut_n=50,
            out_prefix=None, ref='hg38', **args):
    k = int(k)
    cnv_index_name = 'cell_id'
    cnv_df = io.read_cnv_fn(cnv_fn, cnv_index_name)
    cell_names = cnv_df.index.to_list()

    ##### build hc dendrogram #####
    if not nwk_fn:
        newick = phylo.build_hc_tree(cnv_df, cnv_index_name)
        nwk_fn = out_prefix + '.nwk'
        with open(nwk_fn, 'w') as f:
            f.write(newick)
    else:
        newick = open(nwk_fn, 'r').read()
    t = phylo.get_tree_from_newick(newick)

    ##### cut hc dendrogram #####
    cut_t, map_list = phylo.cut_tree(t, k)
    m_df = pd.DataFrame(map_list)
    m_df.columns = [cnv_index_name, 'hcluster']
    m_df.index = m_df[cnv_index_name]
    del m_df[cnv_index_name]

    ##### build nested tree #####
    res = phylo.get_nested_tree_json(t, cut_n)
    json_fn = out_prefix + '_cut{}.json'.format(cut_n)
    with open(json_fn, 'w') as f:
        f.write(res)

    ##### append meta info #####
    if meta_fn:
        meta_df = io.read_meta_fn(meta_fn, cnv_index_name)
        meta_df = pd.merge(meta_df, m_df, how='outer', on=cnv_index_name)
    else:
        meta_df = m_df

    # PCA
    df = embedding.get_pca(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)
    # TSNE
    df = embedding.get_tsne(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)
    # UMAP
    df = embedding.get_umap(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)

    meta_fn = out_prefix + '_meta_scvar.csv'
    meta_df.to_csv(meta_fn)

    ##### build tree by meta category label #####
    evo_trees = {}
    evo_dict = {}
    for col in meta_df.columns:
        if col.startswith('e_') or col.startswith('c_'):
            continue
        df = pd.merge(meta_df[col].apply(str), cnv_df, how='outer', on=cnv_index_name)
        df = df.groupby(col).mean()
        col_fn = out_prefix + '_{}_cnv.csv'.format(col)
        df.to_csv(col_fn)

        t = phylo.build_tree(df)
        ''' # pick, normal, build hc tree
        normal, _ = phylo.choose_normal(df)
        tumor_df = df[~df.index.isin([normal])]
        newick = phylo.build_hc_tree(tumor_df, col)
        t = phylo.get_tree_from_newick(newick, root=normal)
        # evo_dict[col] = phylo.get_evo_tree_dict(t, meta_df[col])
        # t = phylo.reroot_normal(t, df)
        t = phylo.reroot_tree(t, df)
        '''
        evo_trees[col] = t
        annotate_shifts(t, cnv_df, target_gene_fn=target_gene_fn, ref=ref)
        evo_dict[col] = phylo.get_evo_tree_dict(t, meta_df[col], cnv_df.columns.tolist())

    res = json.dumps(evo_dict, indent=4)
    json_fn = out_prefix + '_evo{}.json'.format(k)
    with open(json_fn, 'w') as f:
        f.write(res)

    ###### output evo bin shifts ########
    evo_fn = out_prefix + '_evo{}.tsv'.format(k)
    with open(evo_fn, 'w') as f:
        f.write('\t'.join(['category_label', 'parent', 'child', 'amp/loss', 'region', 'parent_cnv', 'child_cnv', 'shift', 'gene'])+'\n')
        for label, t in evo_trees.items():
            f.write(get_tree_link_tsv(label, t))


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
