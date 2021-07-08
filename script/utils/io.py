import csv
import pandas as pd
import numpy as np


def read_cnv_fn(cnv_fn, index_name):
    if type(cnv_fn) != str:
        return cnv_fn
    df = pd.read_csv(cnv_fn, index_col=0)
    df = df.fillna(2)
    df.index.name = index_name
    return df


def read_cnv_fn_from_loupe(cnv_fn, group_meta_fn, region_meta_fn, confidence):
    group_meta_df = pd.read_csv(group_meta_fn).set_index('group')

    region_meta_df = pd.read_csv(region_meta_fn).set_index('labels').T
    low_regions = region_meta_df[region_meta_df.confidence < confidence].index

    cnv_df = pd.read_csv(cnv_fn)
    cnv_df = cnv_df.set_index('node_id').drop(columns=['num_cells', 'num_noisy'])

    cnv_df.index.name = 'group'
    cnv_df = cnv_df.loc[group_meta_df.index]
    cnv_df = pd.merge(group_meta_df, cnv_df, on='group').drop(columns='num_cells')
    group2cell = cnv_df.groupby('label')['barcodes'].apply(lambda x: ';'.join(x)).to_dict()
    group2cell = {group: cell_str.split(';') for group, cell_str in group2cell.items()}

    cnv_df = cnv_df.groupby('label').mean()

    cnv_df[low_regions] = np.nan
    cnv_df.columns = [c.replace(',', '') for c in cnv_df.columns]
    return group_meta_df, cnv_df, group2cell


def read_meta_fn(meta_fn, index_name='cell_id'):
    df = pd.read_csv(meta_fn, index_col=index_name)
    return df


def read_target_gene(target_gene_fn):
    genes = []
    for line in open(target_gene_fn, 'r'):
        genes.append(line.strip().split('\t')[3])
    genes.sort()
    return genes


def read_10x_bed_fn(bed_fn, confidence=15):
    bed_file = filter(lambda row: row.startswith('#chrom') or not row.startswith('#'), open(bed_fn, 'r'))
    for i, row in enumerate(csv.DictReader(bed_file, delimiter='\t')):
        if int(row.get('event_confidence', confidence)) < confidence:
            continue
        if row['copy_number'] == 'NA':
            continue
        chrom, start, end, cell_id, cn = row['#chrom'], row['start'], row['end'], row['id'], row['copy_number']
        if not chrom.startswith('chr'):
            chrom = 'chr' + chrom
        yield chrom, int(start), int(end), cell_id, int(cn)
