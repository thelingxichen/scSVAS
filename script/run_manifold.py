import torch
import DeepMF
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA, FastICA, NMF
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import datasets
import scprep
# import simu_impute
from utils import embedding
sns.set()


def make_swiss_roll(M, N):
    X, color = datasets.samples_generator.make_swiss_roll(n_samples=M, noise=0.5,
                                                          random_state=2019)
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
    X, color = datasets.samples_generator.make_s_curve(M, random_state=2019)
    data = np.zeros((M, N))
    for i in range(N):
        if i % 2 == 0:
            data[:, i] = X[:, 0]
        else:
            data[:, i] = X[:, 2]
    data += abs(data.min())
    return data, color


def main():

    M, N = int(sys.argv[1]), int(sys.argv[2])
    # data_type = sys.argv[3]
    if not os.path.exists('manifold/{}_{}'.format(M, N)):
        os.makedirs('manifold/{}_{}'.format(M, N))

    '''
    prefix = 'manifold/{}_{}/swiss_roll'.format(M, N)
    o_data, color = make_swiss_roll(M, N)
    run(o_data, color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)


    prefix = 'manifold/{}_{}/circles'.format(M, N)
    o_data, color = make_circles(M, N)
    run(o_data, color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/moons'.format(M, N)
    o_data, color = make_moons(M, N)
    run(o_data, color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/aniso'.format(M, N)
    o_data, color = make_aniso(M, N)
    run(o_data, color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/s_curve'.format(M, N)
    o_data, color = make_s_curve(M, N)
    run(o_data, color, color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)
    '''

    prefix = 'manifold/{}_{}/swiss_roll_circles_dot'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_circles(N, 2)
    V = V.T
    o_data = np.matmul(U, V)
    run(U, V.T, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/swiss_roll_circles_L2'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_circles(N, 2)
    o_data = pairwise_distances(U, V, metric='l2')
    run(U, V, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/swiss_roll_moons_dot'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_moons(N, 2)
    V = V.T
    o_data = np.matmul(U, V)
    run(U, V.T, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/swiss_roll_moons_L2'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_moons(N, 2)
    o_data = pairwise_distances(U, V, metric='l2')
    run(U, V, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/swiss_roll_blobs_dot'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_blobs(N, 2)
    V = V.T
    o_data = np.matmul(U, V)
    run(U, V.T, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/swiss_roll_blobs_L2'.format(M, N)
    U, U_color = make_swiss_roll(M, 2)
    V, V_color = make_blobs(N, 2)
    o_data = pairwise_distances(U, V, metric='l2')
    run(U, V, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/blobs_blobs_dot'.format(M, N)
    U, U_color = make_blobs(M, 2)
    V, V_color = make_blobs(N, 2)
    V = V.T
    o_data = np.matmul(U, V)
    run(U, V.T, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)

    prefix = 'manifold/{}_{}/blobs_blobs_L2'.format(M, N)
    U, U_color = make_blobs(M, 2)
    V, V_color = make_blobs(N, 2)
    o_data = pairwise_distances(U, V, metric='l2')
    run(U, V, o_data, U_color, V_color, prefix)
    np.savetxt('{}.txt'.format(prefix), o_data)


def run(U, V, o_data, U_color, V_color, prefix):
    data = o_data

    f, axes = plt.subplots(5, 4, figsize=(20, 20))
    axs = axes.ravel()

    sns.heatmap(data, cmap='rainbow', xticklabels=False, yticklabels=False, ax=axs[0]).set(title='Y')
    scprep.plot.scatter2d(U, c=U_color, title="U", legend=False, ax=axs[1])
    scprep.plot.scatter2d(V, c=V_color, title="V", legend=False, ax=axs[2])

    U, V, y_pred = run_DeepMF(o_data, prefix+'.DeepMF')
    V = V.T
    sns.heatmap(y_pred, cmap='rainbow', xticklabels=False, yticklabels=False, ax=axs[3]).set(title='DeepMF Y')
    scprep.plot.scatter2d(U, c=U_color, title="DeepMF U", legend=False, ax=axs[7])
    scprep.plot.scatter2d(V, c=V_color, title="DeepMF V", legend=False, ax=axs[11])

    # o_data = simu_impute.random_missing(o_data, 0)
    data = np.nan_to_num(data)

    # PCA
    scprep.plot.scatter2d(embedding.get_pca(data), c=U_color, title="PCA U", legend=False, ax=axs[4])
    scprep.plot.scatter2d(embedding.get_pca(data.T), c=V_color, title="PCA V", legend=False, ax=axs[8])

    # FastICA
    scprep.plot.scatter2d(embedding.get_ica(data), c=U_color, title="ICA U", legend=False, ax=axs[5])
    scprep.plot.scatter2d(embedding.get_ica(data.T), c=V_color, title="ICA V", legend=False, ax=axs[9])

    # NMF
    scprep.plot.scatter2d(embedding.get_nmf(data), c=U_color, title="NMF U", legend=False, ax=axs[6])
    scprep.plot.scatter2d(embedding.get_nmf(data.T), c=V_color, title="NMF V", legend=False, ax=axs[10])

    # TSNE
    scprep.plot.scatter2d(embedding.get_tsne(data), c=U_color, title="TSNE U", legend=False, ax=axs[12])
    scprep.plot.scatter2d(embedding.get_tsne(data.T), c=V_color, title="TSNE V", legend=False, ax=axs[16])

    # UMAP
    scprep.plot.scatter2d(embedding.get_umap(data), c=U_color, title="UMAP U", legend=False, ax=axs[13])
    scprep.plot.scatter2d(embedding.get_umap(data.T), c=V_color, title="UMAP V", legend=False, ax=axs[17])

    # PHATE
    scprep.plot.scatter2d(embedding.get_phate(data), c=U_color, title="PHATE U", legend=False, ax=axs[14])
    scprep.plot.scatter2d(embedding.get_phate(data.T), c=V_color, title="PHATE V", legend=False, ax=axs[18])

    axs[15].set_axis_off()
    axs[19].set_axis_off()

    plt.tight_layout()
    plt.savefig('{}.png'.format(prefix))


def run_DeepMF(data, prefix):
    M, N = data.shape
    device = torch.device("cpu")
    L = 1
    K = 2
    n_batch = 10000
    epoches = 10000

    model = DeepMF.DeepMF(M, N, K=K, L=L,
                          learning_rate=1e-3,
                          epoches=epoches,
                          neighbor_proximity='KL',
                          neighbor_k=5,
                          device=device, problem='regression', data_type='impute', prefix=prefix)

    model.fit(data, n_batch, alpha=0.01)

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
