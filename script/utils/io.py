
import pandas as pd


def read_cnv_fn(cnv_fn, index_name):
    df = pd.read_csv(cnv_fn, index_col=0)
    df = df.fillna(2) 
    df.index.name = index_name 
    return df


def read_meta_fn(meta_fn, index_name):
    df = pd.read_csv(meta_fn, index_col=index_name)
    return df


def read_target_gene(target_gene_fn):
    genes = []
    for line in open(target_gene_bed_fn, 'r'):
        genes.append(line.strip().split('\t')[3])
    genes.sort()
    return genes


