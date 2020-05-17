import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import scprep
import phate
import os

import DeepMF
from utils import embedding


def get_tree():
    data, color = phate.tree.gen_dla(n_dim=200, n_branch=10, branch_length=30,
                                     rand_multiplier=2, seed=37, sigma=5)
    data = data + np.abs(np.min(data))
    return data, color


def run_embedding(df, index, index_name):
    phate_df = embedding.get_phate(df, index, index_name)
    tsne_df = embedding.get_tsne(df, index, index_name)
    umap_df = embedding.get_umap(df, index, index_name)
    pca_df = embedding.get_pca(df, index, index_name)
    return pca_df, tsne_df, umap_df, phate_df


def run(data, color, prefix, L, K, epoches, alpha, device, neighbor_k, learning_rate):

    f, axes = plt.subplots(2, 3, figsize=(9, 6))
    axs = axes.ravel()

    # plotting data
    # sns.heatmap(data, cmap="rainbow", xticklabels=False, yticklabels=False, ax=axs[0]).set(title='Y')

    U, V, y_pred = DeepMF.run_DeepMF(data, prefix+'.DeepMF', L, K, epoches, alpha, device, neighbor_k, learning_rate)
    V = V.T

    # plotting y_pred
    # sns.heatmap(y_pred, cmap="rainbow", xticklabels=False, yticklabels=False, ax=axs[1]).set(title='predicted Y')

    # PCA
    scprep.plot.scatter2d(embedding.get_pca(data), c=color, cmap='rainbow', title="PCA", legend=False, ax=axs[0])

    # FastICA
    scprep.plot.scatter2d(embedding.get_ica(data), c=color, cmap='rainbow', title="ICA", legend=False, ax=axs[1])

    # NMF
    scprep.plot.scatter2d(embedding.get_nmf(data), c=color, cmap='rainbow', title="NMF", legend=False, ax=axs[2])

    # TSNE
    scprep.plot.scatter2d(embedding.get_tsne(data), c=color, cmap='rainbow', title="TSNE", legend=False, ax=axs[3])

    # UMAP
    scprep.plot.scatter2d(embedding.get_umap(data), c=color, cmap='rainbow', title="UMAP", legend=False, ax=axs[4])

    # PHATE
    # scprep.plot.scatter2d(embedding.get_phate(data), c=color, cmap='rainbow', title="PHATE", legend=False, ax=axs[5])

    # plotting U
    scprep.plot.scatter2d(U, c=color, cmap='rainbow', title="DeepMF U", legend=False, ax=axs[5])

    plt.tight_layout()
    _, title = os.path.split(prefix)
    # plt.suptitle(title, size=20)
    plt.tight_layout()
    # f.subplots_adjust(top=0.95)
    plt.savefig('{}.png'.format(prefix))


def main():
    if not os.path.exists('latent'):
        os.makedirs('latent')

    data, color = get_tree()
    run(data, color, 'latent/tree', L=3, K=2, epoches=200, alpha=1, device='cpu', neighbor_k=30, learning_rate=1e-1)


if __name__ == "__main__":
    main()
