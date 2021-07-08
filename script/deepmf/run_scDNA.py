import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scprep
import os

import DeepMF
from utils import embedding
from utils import io


def get_cnv_data(cnv_fn, meta_fn, cluster_label):
    index_name = 'cell_id'
    cnv_df = io.read_cnv_fn(cnv_fn, index_name)
    meta_df = io.read_meta_fn(meta_fn, index_name)

    return cnv_df.to_numpy(), meta_df[cluster_label]


def run(data, color, prefix, L, K, epoches, alpha, device, neighbor_k, learning_rate, neighbor_proximity):

    f, axes = plt.subplots(3, 3, figsize=(9, 9))
    axs = axes.ravel()

    U, V, y_pred = DeepMF.run_DeepMF(data, prefix+'.DeepMF', L, K, epoches, alpha, device, neighbor_k, learning_rate, neighbor_proximity)
    U_df = pd.DataFrame(U, columns=['e_DeepMF_U1', 'e_DeepMF_U2'])
    V = V.T

    # PCA
    scprep.plot.scatter2d(embedding.get_pca(data), c=color, cmap='rainbow', title="PCA", legend=True, ax=axs[0])

    # FastICA
    scprep.plot.scatter2d(embedding.get_ica(data), c=color, cmap='rainbow', title="ICA", legend=False, ax=axs[1])

    # NMF
    scprep.plot.scatter2d(embedding.get_nmf(data), c=color, cmap='rainbow', title="NMF", legend=False, ax=axs[2])

    # TSNE
    scprep.plot.scatter2d(embedding.get_tsne(data), c=color, cmap='rainbow', title="TSNE", legend=False, ax=axs[3])

    # UMAP
    scprep.plot.scatter2d(embedding.get_umap(data), c=color, cmap='rainbow', title="UMAP", legend=False, ax=axs[4])

    # PHATE
    scprep.plot.scatter2d(embedding.get_phate(data), c=color, cmap='rainbow', title="PHATE", legend=False, ax=axs[5])

    # plotting U
    scprep.plot.scatter2d(U_df, c=color, cmap='rainbow', title="DeepMF U", legend=False, ax=axs[6])

    # plotting data
    sns.heatmap(data, cmap="rainbow", xticklabels=False, yticklabels=False, ax=axs[7]).set(title='Y')

    # plotting y_pred
    sns.heatmap(y_pred, cmap="rainbow", xticklabels=False, yticklabels=False, ax=axs[8]).set(title='DeepMF Y')

    plt.tight_layout()
    _, title = os.path.split(prefix)
    # plt.suptitle(title, size=20)
    plt.tight_layout()
    # f.subplots_adjust(top=0.95)
    plt.savefig('{}.png'.format(prefix))


def main():
    if not os.path.exists('scDNA'):
        os.makedirs('scDNA')

    # data, color = get_cnv_data(os.path.join('..', 'demo_data', 'demo_chr22_cnv.csv'), os.path.join('..', 'demo_data', 'demo_chr22_meta.csv'), 'cluster')
    # run(data, color, 'scDNA/demo_chr22', L=1, K=2, epoches=5000, alpha=0.01, device='cpu', neighbor_k=3, learning_rate=1e-1)

    data, color = get_cnv_data(os.path.join('..', 'demo_data', 'T10_cnv.csv'), os.path.join('../', 'demo_data', 'T10_meta.csv'), 'group')
    run(data, color, 'scDNA/T10', L=2, K=2, epoches=1000, alpha=0.01, device='cuda', neighbor_k=5, learning_rate=1e-2, neighbor_proximity='KL')

    data, color = get_cnv_data(os.path.join('..', 'demo_data', 'T16_cnv.csv'), os.path.join('../', 'demo_data', 'T16_meta.csv'), 'group2')
    run(data, color, 'scDNA/T16', L=2, K=2, epoches=1000, alpha=0.01, device='cuda', neighbor_k=5, learning_rate=1e-2, neighbor_proximity='KL')


if __name__ == "__main__":
    main()
