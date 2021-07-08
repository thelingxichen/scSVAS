import numpy as np
import pandas as pd
from ete3 import Tree


def process_tree(tree_fn):

    tree_df = pd.read_csv(tree_fn)
    source = tree_df['source'].values
    target = tree_df['target'].values

    root = set(source) - set(target)
    root = root.pop()

    t = build_tree(root, tree_df, None)

    node_list = sorted(t.nodes, key=lambda n: n.dist_to_root)
    node_dict = {n.name: n for n in node_list}
    node_name_list = [n.name for n in node_list]
    return t, node_dict, node_name_list


def build_tree(node, tree_df, parent_t):
    t = Tree()
    if 'distance' in tree_df.columns:
        t.dist = 1
    else:
        t.dist = 1
    if parent_t:
        t.dist_to_root = parent_t.dist_to_root + t.dist
    else:
        t.dist_to_root = 0
    t.name = node
    t.parent = parent_t
    childs = tree_df[tree_df['source'] == node]['target'].values.tolist()
    if childs:
        t.children = [build_tree(c, tree_df, t) for c in childs]
    else:
        t.children = []
    t.nodes = [t] + sum([c.nodes for c in t.children], [])
    return t


def get_linkage_matrix(t, nodes_dict, node_name_list):
    N = len(t.nodes)
    m = np.zeros((N, N))
    for n in t.nodes:
        if not n.parent:
            continue
        i = node_name_list.index(n.parent.name)
        j = node_name_list.index(n.name)
        m[i, j] = 1
    return m


def get_prev_df(prev_fn, node_name_list, low_prev_thresh=0.01):
    df = pd.read_csv(prev_fn)
    df = df.pivot(index='sample_id', columns='clone_id', values='clonal_prev')
    df = df[node_name_list]
    if low_prev_thresh > 0:
        df[df < low_prev_thresh] = 0
        df[df >= low_prev_thresh] = 1
    df = df.sort_values(by=node_name_list)
    return df


def get_dist_df(node_dict, node_name_list):
    N = len(node_name_list)
    m = np.zeros((N, N))
    for i, name_i in enumerate(node_name_list):
        n_i = node_dict[name_i]
        for j, name_j in enumerate(node_name_list):
            n_j = node_dict[name_j]
            m[i, j] = abs(n_i.dist_to_root - n_j.dist_to_root)
    df = pd.DataFrame(data=m, columns=node_name_list, index=node_name_list)
    return df


def predict_sample_dist_df(prev_df, clone_dist_df):
    sample_name_list = prev_df.index
    M, N = prev_df.shape
    P = prev_df.to_numpy()
    D_c = clone_dist_df.to_numpy()
    m = np.zeros((M, M))
    for i1 in range(M):
        for i2 in range(M):
            # print('i1, i2 = ', i1, i2)
            a, b = 0, 0
            for j1 in range(N):
                for j2 in range(N):
                    a += P[i1, j1] * P[i2, j2] * D_c[j1, j2]
                    b += P[i1, j1] * P[i2, j2]

            # print('a, b = ', a, b)
            if i1 != i2:
                m[i1, i2] = a / b

    df = pd.DataFrame(data=m, columns=sample_name_list, index=sample_name_list)
    return df


def get_minimal_spanning_tree(dist_df):

    root = dist_df.index[0]

    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import minimum_spanning_tree
    X = dist_df.to_numpy()
    X = csr_matrix(X)
    Tcsr = minimum_spanning_tree(X)
    print(Tcsr.toarray().astype(int))


def run(prev_fn, clone_tree_fn, sample_tree_fn):
    _, clone_node_dict, clone_node_name_list = process_tree(clone_tree_fn)

    prev_df = get_prev_df(prev_fn, clone_node_name_list, low_prev_thresh=0.01)
    clone_node_name_list = prev_df.columns
    clone_dist_df = get_dist_df(clone_node_dict, clone_node_name_list)

    sample_t, sample_node_dict, _ = process_tree(sample_tree_fn)
    sample_node_name_list = prev_df.index
    sample_dist_df = get_dist_df(sample_node_dict, sample_node_name_list)

    pred_sample_dist_df = predict_sample_dist_df(prev_df, clone_dist_df)

    get_minimal_spanning_tree(pred_sample_dist_df)
    get_minimal_spanning_tree(sample_dist_df)

    print(get_linkage_matrix(sample_t, sample_node_dict, sample_node_name_list.to_list()))

    plot(prev_df, clone_dist_df, pred_sample_dist_df, sample_dist_df)


def plot(prev_df, clone_dist_df, pred_sample_dist_df, sample_dist_df):
    from matplotlib import pyplot as plt
    import seaborn as sns

    f, axes = plt.subplots(2, 3, figsize=(9, 6))
    axs = axes.ravel()
    cmap = 'YlOrRd'

    sns.heatmap(prev_df, cmap=cmap, ax=axs[0]).set(title='clonal prevelance matrix, P')
    sns.heatmap(clone_dist_df, cmap=cmap, ax=axs[1]).set(title='clone distance matrix, D^c')
    axs[2].set_axis_off()
    sns.heatmap(pred_sample_dist_df, cmap=cmap, ax=axs[3]).set(title='sample distance matrix, pred_D^l')
    sns.heatmap(sample_dist_df, cmap=cmap, ax=axs[4]).set(title='sample distance matrix, D^l')
    sns.heatmap(abs(sample_dist_df/sample_dist_df.max().max()-pred_sample_dist_df/pred_sample_dist_df.max().max()),
                cmap=cmap, ax=axs[5]).set(title='D^l - pred_D^l')

    plt.tight_layout()
    plt.savefig('space_lineage.png')


'''
prev_fn = '../demo_data/A21_clonal_prev.csv'
clone_tree_fn = '../demo_data/A21_tree.csv'
sample_tree_fn = '../demo_data/A21_space_tree.csv'


run(prev_fn, clone_tree_fn, sample_tree_fn)
'''
