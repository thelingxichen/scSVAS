import pysam
import pandas as pd
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam', help='Input BAM file')
    parser.add_argument('--out-root', help='Root directory to write output BAMs to')
    parser.add_argument('--csv', help='CSV file with two columns: barcode and group.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    df = pd.read_csv(args.csv)
    assert 'barcode' in df.columns and 'group' in df.columns, 'Missing column identifiers'
    assert os.path.exists(args.bam), 'Cannot find input BAM'
    fh = pysam.Samfile(args.bam)
    group_map = dict(zip(df.barcode, df.group))
    if not os.path.exists(args.out_root):
        os.makedirs(args.out_root)
    out_handles = {}
    for c in set(df.group):
        o = pysam.Samfile(os.path.join(args.out_root, 'group' + str(c) + '.bam'),
                          'wb', template=fh)
        out_handles[c] = o

    for c in set(df.group):
        for rec in fh:
            if rec.has_tag('CB') and rec.get_tag('CB') in group_map:
                group = group_map[rec.get_tag('CB')]
                out_handles[group].write(rec)

    for h in out_handles.values():
        h.close()
