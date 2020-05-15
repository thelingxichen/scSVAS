import matplotlib.pyplot as plt
import seaborn as sns
import scprep


from utils import embedding


def run_embedding(df, index, index_name):
    phate_df = embedding.get_phate(df, index, index_name)
    tsne_df = embedding.get_tsne(df, index, index_name)
    umap_df = embedding.get_umap(df, index, index_name)
    pca_df = embedding.get_pca(df, index, index_name)
    return pca_df, tsne_df, umap_df, phate_df


def plot_embedding(data, y_pred, U_df, V, meta_df, cluster_label, pca_df, tsne_df, umap_df, phate_df):

    f, axes = plt.subplots(2, 4, figsize=(16, 8))
    ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8 = axes.ravel()

    # plotting data
    sns.heatmap(data, cmap="rainbow", xticklabels=False, yticklabels=False, ax=ax1).set(title='Y')

    # plotting y_pred
    sns.heatmap(y_pred, cmap="rainbow", xticklabels=False, yticklabels=False, ax=ax2).set(title='predicted Y')

    # plotting U
    scprep.plot.scatter2d(U_df, c=meta_df[cluster_label], title="DeepMF U", legend=False, ax=ax3)

    # plotting V
    sns.heatmap(V, cmap="rainbow", xticklabels=False, yticklabels=False, ax=ax4).set(title='DeepMF V')

    scprep.plot.scatter2d(pca_df, c=meta_df[cluster_label], title="PCA", legend=False, ax=ax5)

    scprep.plot.scatter2d(tsne_df, c=meta_df[cluster_label], title="TSNE", legend=False, ax=ax6)

    scprep.plot.scatter2d(umap_df, c=meta_df[cluster_label], title="UMAP", legend=False, ax=ax7)

    scprep.plot.scatter2d(phate_df, c=meta_df[cluster_label], title="PHATE", legend=False, ax=ax8)

    plt.tight_layout()
