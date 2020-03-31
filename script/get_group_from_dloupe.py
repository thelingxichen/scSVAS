import os
import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--heatmap_cn', help='Input 10x dloupe root node heatmap cn file')
    parser.add_argument('--summary', help='Input 10x cellranger per cell summary file')
    parser.add_argument('--min_cells', help='Minimum cells number of group.',
                        default=10)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    summary_df = pd.read_csv(args.summary)
    assert 'barcode' in summary_df.columns and 'is_noisy' in summary_df.columns, 'Missing column identifiers'
    cnv_df = pd.read_csv(args.heatmap_cn)
    assert 'node_id' in cnv_df.columns and 'barcodes' in cnv_df.columns, 'Missing column identifiers'

    summary_df = summary_df[summary_df.is_noisy == 0]
    barcodes = summary_df.barcode.to_list()

    cnv_df = cnv_df[cnv_df.num_cells - cnv_df.num_noisy >= args.min_cells]
    cnv_df = cnv_df[['barcodes', 'node_id']]
    reshaped = \
        (cnv_df.set_index(cnv_df.columns.drop('barcodes', 1).tolist())
            .barcodes.str.split(';', expand=True)
            .stack()
            .reset_index()
            .rename(columns={0: 'barcodes'})
            .loc[:, cnv_df.columns]
         )
    cnv_df = reshaped[reshaped.barcodes.isin(barcodes)]
    cnv_df.columns = ['barcode', 'group']

    out_dir, _ = os.path.split(args.summary)
    cnv_df.to_csv(os.path.join(out_dir, 'barcode_group.csv'))
