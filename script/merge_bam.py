import pysam
import pandas as pd
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_dir', help='Input BAM file directory')
    parser.add_argument('--out-root', help='Root directory to write output BAMs to')
    parser.add_argument('--csv', help='CSV file with two columns: cell_id and group.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    df = pd.read_csv(args.csv)
    assert 'cell_id' in df.columns and 'group' in df.columns, 'Missing column identifiers'
    assert os.path.exists(args.bam_dir), 'Cannot find input BAM directory'
    group_map = dict(zip(df.cell_id, df.group))

    if not os.path.exists(args.out_root):
        os.makedirs(args.out_root)

    fn = [x for x in os.listdir(args.bam_dir) if x.endswith('.bam')][0]
    temp_fh = pysam.Samfile(os.path.join(args.bam_dir, fn))

    out_handles = {}
    for c in set(df.group):
        o = pysam.Samfile(os.path.join(args.out_root, 'group' + str(c) + '.bam'),
                          'wb', template=temp_fh)
        out_handles[c] = o

    for cell_id, group in group_map.items():
        fh = pysam.Samfile(os.path.join(args.bam_dir,
                                        '{}.bam'.format(cell_id)))
        for rec in fh:
            out_handles[group].write(rec)

    for h in out_handles.values():
        h.close()
