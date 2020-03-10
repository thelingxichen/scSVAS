import pybedtools
import csv
import os
import numpy as np
import pandas as pd


def read_target_gene(target_gene_bed_fn):
    genes = []
    for line in open(target_gene_bed_fn, 'r'):
        genes.append(line.strip().split('\t')[3])
    genes.sort()
    return genes


def main(in_dir):
    target_gene_bed_fn = 'target_gene.bed'
    target_genes = read_target_gene(target_gene_bed_fn)
    num_genes = len(target_genes)
    cnv_bed_fn = os.path.join(in_dir, 'node_cnv_calls.bed')
    summary_fn = os.path.join(in_dir, 'summary.csv')
    for row in csv.DictReader(open(summary_fn, 'r')):
        num_cells = int(row['num_cells'])
    m = np.zeros((num_cells, num_genes))
    m[:] = np.nan

    a = pybedtools.BedTool(target_gene_bed_fn)
    b = pybedtools.BedTool(cnv_bed_fn)
    # b = b.filter(lambda x: int(x[4]) != 2 and int(x[5]) > 15)
    b = b.filter(lambda x: int(x[5]) > 15)

    hits = a.window(b).overlap(cols=[2, 3, 6, 7])
    for x in hits:
        gene = x[3]
        cell_id = int(x[7])
        cn = int(x[8])
        if cell_id > num_cells:
            continue
        m[cell_id-1, target_genes.index(gene)] = cn
    df = pd.DataFrame(m)
    df.columns = target_genes
    out_fn = os.path.join(in_dir, 'target_gene_cnv.csv')
    df.to_csv(out_fn)


if __name__ == "__main__":
    for i in range(1, 10):
        in_dir = '2019jz0{}'.format(i)
        main(in_dir)
