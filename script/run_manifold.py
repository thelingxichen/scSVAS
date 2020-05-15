import torch
import DeepMF
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import datasets
import scprep
# import simu_impute
from utils import embedding
sns.set_style("white")


def make_swiss_roll(M, N):
    X, color = datasets.make_swiss_roll(n_samples=M, noise=0.5, random_state=2019)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 2]
    data += abs(data.min())
    data = data/data.max()
    return data, color


def make_circles(M, N):
    X, color = datasets.make_circles(n_samples=M, factor=.5, noise=.05,
                                     random_state=2019)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 1]
    data += abs(data.min())
    return data, color


def make_moons(M, N):
    X, color = datasets.make_moons(n_samples=M, noise=.05, random_state=2019)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 1]
    data += abs(data.min())
    return data, color


def make_aniso(M, N):
    X, color = datasets.make_blobs(n_samples=M, n_features=2, cluster_std=0, random_state=2019,
                                   centers=[[1, 1], [3, 2]])
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X = np.dot(X, transformation)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 1]
    data += abs(data.min())
    data = data/data.max()
    return data, color


def make_blobs(M, N):
    X, color = datasets.make_blobs(n_samples=M, n_features=2, cluster_std=0.1, shuffle=False,
                                   random_state=2019,
                                   centers=[[1, 1], [3, 2]])
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 1]
    data += abs(data.min())
    data = data/data.max()
    return data, color


def make_s_curve(M, N):
    X, color = datasets.make_s_curve(M, random_state=2019)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 2]
    data += abs(data.min())
    return data, color


def run_pair(M, N, U_pattern, V_pattern, func, L, K, epoches, alpha):
    prefix = 'manifold/{}_{}/{}_{}_{}'.format(M, N, U_pattern, V_pattern, func)
    u_func = globals()['make_' + U_pattern]
    v_func = globals()['make_' + V_pattern]
    U, U_color = u_func(M, 2)
    V, V_color = v_func(N, 2)
    if func == 'dot':
        o_data = np.matmul(U, V.T)
    if func == 'L2':
        o_data = pairwise_distances(U, V, metric='l2')
    run(U, V, o_data, U_color, V_color, prefix, L, K, epoches, alpha)
    np.savetxt('{}.txt'.format(prefix), o_data)


def main():

    M, N = int(sys.argv[1]), int(sys.argv[2])
    epoches = 10000
    if not os.path.exists('manifold/{}_{}'.format(M, N)):
        os.makedirs('manifold/{}_{}'.format(M, N))

    '''
    blobs and aniso have problem
    L2, non-linear interaction
    '''

    run_pair(M, N, 'swiss_roll', 'swiss_roll', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'swiss_roll', 'swiss_roll', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 'swiss_roll', 'circles', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'swiss_roll', 'circles', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'swiss_roll', 'moons', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'swiss_roll', 'moons', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'swiss_roll', 'aniso', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'swiss_roll', 'aniso', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'swiss_roll', 's_curve', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'swiss_roll', 's_curve', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 'swiss_roll', 'blobs', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'swiss_roll', 'blobs', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'circles', 'circles', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'circles', 'circles', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'circles', 'moons', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'circles', 'moons', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'circles', 'aniso', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'circles', 'aniso', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'circles', 's_curve', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'circles', 's_curve', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 'circles', 'blobs', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'circles', 'blobs', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'moons', 'moons', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'moons', 'moons', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'moons', 'aniso', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'moons', 'aniso', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'moons', 's_curve', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'moons', 's_curve', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 'moons', 'blobs', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'moons', 'blobs', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'aniso', 'aniso', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'aniso', 'aniso', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'aniso', 's_curve', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'aniso', 's_curve', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 'aniso', 'blobs', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 'aniso', 'blobs', 'L2', 1, 2, epoches, 0.01)

    # run_pair(M, N, 's_curve', 's_curve', 'dot', 1, 2, epoches, 0.01)
    # run_pair(M, N, 's_curve', 's_curve', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 's_curve', 'blobs', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 's_curve', 'blobs', 'L2', 1, 2, epoches, 0.01)

    run_pair(M, N, 'blobs', 'blobs', 'dot', 1, 2, epoches, 0.1)
    # run_pair(M, N, 'blobs', 'blobs', 'L2', 1, 2, epoches, 0.01)


def run(U, V, o_data, U_color, V_color, prefix, L, K, epoches, alpha):
    data = o_data

    f, axes = plt.subplots(6, 3, figsize=(10, 20))
    axs = axes.ravel()

    sns.heatmap(data, cmap='rainbow', xticklabels=False, yticklabels=False, ax=axs[0]).set(title='Y')
    scprep.plot.scatter2d(U, c=U_color, cmap='rainbow', title="U", legend=False, ax=axs[1])
    scprep.plot.scatter2d(V, c=V_color, cmap='rainbow', title="V", legend=False, ax=axs[4])

    U, V, y_pred = run_DeepMF(o_data, prefix+'.DeepMF', L, K, epoches, alpha)
    V = V.T
    sns.heatmap(y_pred, cmap='rainbow', xticklabels=False, yticklabels=False, ax=axs[3]).set(title='DeepMF Y')
    scprep.plot.scatter2d(U, c=U_color, cmap='rainbow', title="DeepMF U", legend=False, ax=axs[2])
    scprep.plot.scatter2d(V, c=V_color, cmap='rainbow', title="DeepMF V", legend=False, ax=axs[5])

    # o_data = simu_impute.random_missing(o_data, 0)
    data = np.nan_to_num(data)

    # PCA
    scprep.plot.scatter2d(embedding.get_pca(data), c=U_color, cmap='rainbow', title="PCA U", legend=False, ax=axs[6])
    scprep.plot.scatter2d(embedding.get_pca(data.T), c=V_color, cmap='rainbow', title="PCA V", legend=False, ax=axs[9])

    # FastICA
    scprep.plot.scatter2d(embedding.get_ica(data), c=U_color, cmap='rainbow', title="ICA U", legend=False, ax=axs[7])
    scprep.plot.scatter2d(embedding.get_ica(data.T), c=V_color, cmap='rainbow', title="ICA V", legend=False, ax=axs[10])

    # NMF
    scprep.plot.scatter2d(embedding.get_nmf(data), c=U_color, cmap='rainbow', title="NMF U", legend=False, ax=axs[8])
    scprep.plot.scatter2d(embedding.get_nmf(data.T), c=V_color, cmap='rainbow', title="NMF V", legend=False, ax=axs[11])

    # TSNE
    scprep.plot.scatter2d(embedding.get_tsne(data), c=U_color, cmap='rainbow', title="TSNE U", legend=False, ax=axs[12])
    scprep.plot.scatter2d(embedding.get_tsne(data.T), c=V_color, cmap='rainbow', title="TSNE V", legend=False, ax=axs[15])

    # UMAP
    scprep.plot.scatter2d(embedding.get_umap(data), c=U_color, cmap='rainbow', title="UMAP U", legend=False, ax=axs[13])
    scprep.plot.scatter2d(embedding.get_umap(data.T), c=V_color, cmap='rainbow', title="UMAP V", legend=False, ax=axs[16])

    # PHATE
    scprep.plot.scatter2d(embedding.get_phate(data), c=U_color, cmap='rainbow', title="PHATE U", legend=False, ax=axs[14])
    scprep.plot.scatter2d(embedding.get_phate(data.T), c=V_color, cmap='rainbow', title="PHATE V", legend=False, ax=axs[17])

    _, title = os.path.split(prefix)
    plt.suptitle(title, size=20)
    plt.tight_layout()
    f.subplots_adjust(top=0.95)
    plt.savefig('{}.png'.format(prefix))


def run_DeepMF(data, prefix, L, K, epoches, alpha):
    M, N = data.shape
    device = torch.device("cpu")
    n_batch = 10000

    model = DeepMF.DeepMF(M, N, K=K, L=L,
                          learning_rate=1e-3,
                          epoches=epoches,
                          neighbor_proximity='KL',
                          neighbor_k=5,
                          device=device, problem='regression', data_type='impute', prefix=prefix)

    model.fit(data, n_batch, alpha)

    y_pred = model.predict(data)
    U, V = model.save_U_V()

    return U, V, y_pred


'''
def run_DMF(data, prefix):
    M, N = data.shape
    device = torch.device("cpu")
    L = 5
    K = 2
    n_batch = 10000
    epoches = 1000

    model = DMF.DMF(M, N, K=K, L=L,
                    learning_rate=1e-3,
                    epoches=epoches,
                    device=device, prefix=prefix)

    model.fit(data, n_batch, alpha=0.01)
    y_pred = model.predict(data)

    U, V = model.save_U_V()
    return U, V, y_pred
'''


if __name__ == "__main__":
    main()
