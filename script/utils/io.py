import csv
import pandas as pd


def read_cnv_fn(cnv_fn, index_name):
    if type(cnv_fn) != str:
        return cnv_fn
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
