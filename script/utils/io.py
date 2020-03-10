
def read_cnv_fn(cnv_fn):
    df = pd.read_csv(cnv_fn)
    cell_names = df.values[:, 0]
    cnv_m = df.values[:, 1:]
    return cnv_m, cell_names

def read_meta_fn(meta_fn):
    df = pd.read_csv(meta_fn, index_col='cell_id')
    return df
    
