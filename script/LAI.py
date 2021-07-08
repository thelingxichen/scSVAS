#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    LAI.py loupe --cnv_fn=IN_FILE --group_meta_fn=IN_FILE --region_meta_fn=IN_FILE [--ref=STR] [--confidence=INT] [--out_prefix=STR] [--target_gene_fn=STR] [--tree_fn=IN_FILE]
    LAI.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --cnv_fn=IN_FILE            Path of cnv file.
    --group_meta_fn=IN_FILE     Path of group meta file.
    --region_meta_fn=IN_FILE    Path of region meta file.
    --out_prefix=STR            Path of out file prefix, [default: ./phylo]
    --confidence=INT            CNV event confidence, [default: 5]
    --ref=STR                   Reference version, [default: hg38]
"""
import docopt
import numpy as np
import json

from biotool import genome

from utils import phylogenetic as phylo
from utils import io
from utils import annotation as anno
import spacelineage


''''
annotate bin changes ############
'''


def annotate_shifts(t, cnv_df, shift=0.5, target_gene_fn=None, ref='hg38'):
    cytoband_dict = genome.read_cytoband(ref)

    for link in t.links:
        p_cnv = link.source.cnv
        c_cnv = link.target.cnv

        shifts = np.array(c_cnv) - np.array(p_cnv)
        amp_index = sum(np.argwhere(shifts > shift).tolist(), [])
        loss_index = sum(np.argwhere(shifts < -shift).tolist(), [])
        amp_bins = cnv_df.iloc[:, amp_index].columns.tolist()
        loss_bins = cnv_df.iloc[:, loss_index].columns.tolist()

        amp_bins_dict = deal_shift_dict(amp_bins, amp_index, link)
        loss_bins_dict = deal_shift_dict(loss_bins, loss_index, link)

        link.meta = '{} amp, {} loss'.format(len(amp_bins), len(loss_bins))
        # bin: {gene:[], cnv:[p, c, shift]}
        link.shift_bins = {'amp': amp_bins_dict, 'loss': loss_bins_dict}
        call_bedtool_bin2gene(amp_bins, ref, link=link, shift_type='amp', target_gene_fn=target_gene_fn, cytoband_dict=cytoband_dict)
        call_bedtool_bin2gene(loss_bins, ref, link=link, shift_type='loss', target_gene_fn=target_gene_fn, cytoband_dict=cytoband_dict)


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


def process_bin2gene_hits(bin, hits, link=None, shift_type=None, cytoband_dict=None,
                          **kwargs):
    gene_list = [hit[6].split(',')[0] for hit in hits]
    link.shift_bins[shift_type][bin]['gene'] = gene_list

    cytoband = genome.get_cytoband_from_bin_str(cytoband_dict, bin)
    link.shift_bins[shift_type][bin]['cytoband'] = cytoband


def run_loupe(cnv_fn=None, group_meta_fn=None, region_meta_fn=None, out_prefix=None, confidence=None,
              tree_fn=None,
              ref='hg38', target_gene_fn=None, **args):
    confidence = int(confidence)
    confidence = 5
    group_meta_df, cnv_df, group2cell = io.read_cnv_fn_from_loupe(cnv_fn, group_meta_fn, region_meta_fn, confidence)
    # build tree by meta category label #####
    evo_trees = {}
    evo_dict = {}
    col = 'label'
    if tree_fn:
        t, _, _ = spacelineage.process_tree(tree_fn)
        phylo.set_tree(t, prefix=None)
        for n in t.nodes:
            if n.name in cnv_df.index:
                n.cnv = cnv_df.loc[n.name].tolist()
            else:
                tmp = t.nodes[1]
                n.cnv = [c if np.isnan(c) else 2 for c in cnv_df.loc[tmp.name].tolist()]
            n.cells = group2cell.get(n.name, [])
    else:
        t = phylo.build_tree(cnv_df, group2cell, merge=False)
    evo_trees[col] = t

    col_fn = out_prefix + '_{}_cnv.csv'.format(col)
    cnv_df.to_csv(col_fn)

    # annotate_shifts(t, cnv_df, target_gene_fn=target_gene_fn, ref=ref)
    evo_dict[col] = phylo.get_evo_tree_dict(t, group_meta_df[col], cnv_df.columns.tolist())

    res = json.dumps(evo_dict, indent=4)
    json_fn = out_prefix + '_evo.json'
    with open(json_fn, 'w') as f:
        f.write(res)

    '''
    # output evo bin shifts ########
    evo_fn = out_prefix + '_evo.tsv'
    with open(evo_fn, 'w') as f:
        f.write('\t'.join(['category_label', 'parent', 'child', 'amp/del', 'region', 'cytoband', 'parent_cnv', 'child_cnv', 'shift', 'gene'])+'\n')
        for label, t in evo_trees.items():
            f.write(get_tree_link_tsv(label, t))
    '''


def get_tree_link_tsv(label, t):
    res = ''
    for link in t.links:
        for bin, bin_dict in link.shift_bins['amp'].items():
            p, c, s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            if 'gene' not in bin_dict:
                continue
            gene_str = ','.join(bin_dict.get('gene', []))
            cytoband = bin_dict.get('cytoband', '')
            r = [label, link.source.name, link.target.name, 'amp', bin, cytoband, p, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
        for bin, bin_dict in link.shift_bins['loss'].items():
            p, c, s = bin_dict['cnv'][0], bin_dict['cnv'][1], bin_dict['cnv'][2]
            if 'gene' not in bin_dict:
                continue
            gene_str = ','.join(bin_dict.get('gene', []))
            cytoband = bin_dict.get('cytoband', '')
            r = [label, link.source.name, link.target.name, 'loss', bin, cytoband, p, c, s, gene_str]
            res += '\t'.join(map(str, r)) + '\n'
    return res


def run(loupe=None, **args):
    if loupe:
        run_loupe(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
