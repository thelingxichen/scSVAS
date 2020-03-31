import pysam
import pandas as pd
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_dir', help='Input BAM file directory')
    parser.add_argument('--out-root', help='Root directory to write output BAMs to')
    parser.add_argument('--csv', help='CSV file with two columns: barcode and group.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    df = pd.read_csv(args.csv)
    assert 'barcode' in df.columns and 'group' in df.columns, 'Missing column identifiers'
    assert os.path.exists(args.bam_dir), 'Cannot find input BAM directory'
    group_map = dict(zip(df.barcode, df.group))

    if not os.path.exists(args.out_root):
        os.makedirs(args.out_root)

    temp_fh = pysam.Samfile(os.path.join(args.bam_dir, 'A',
                                         'AAATGCCTCCCGTTGT-1.bam'))
    out_handles = {}
    for c in set(df.group):
        o = pysam.Samfile(os.path.join(args.out_root, 'group' + str(c) + '.bam'),
                          'wb', template=temp_fh)
        out_handles[c] = o

    for barcode, group in group_map.items():
        bc, section = barcode.split('-')
        section = {'1': 'A', '2': 'B',
                   '3': 'C', '4': 'D',
                   '5': 'E'}[section]

        fh = pysam.Samfile(os.path.join(args.bam_dir, section,
                                        '{}-1.bam'.format(bc)))
        for rec in fh:
            rec.set_tag('CB', barcode)
            out_handles[group].write(rec)

    for h in out_handles.values():
        h.close()
