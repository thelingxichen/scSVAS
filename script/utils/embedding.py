#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Embedding Map
'''

import pandas as pd
from sklearn.decomposition import PCA, FastICA, NMF
from sklearn.manifold import TSNE, MDS, SpectralEmbedding, Isomap, LocallyLinearEmbedding
from umap import UMAP
from phate import PHATE
from pydiffmap.diffusion_map import DiffusionMap

# linear dimension reduction


def get_tsne(m, index=None, index_name='index', perplexity=30):
    df = pd.DataFrame(TSNE(n_components=2, init='pca', random_state=0).fit_transform(m), columns=['e_TSNE1', 'e_TSNE2'])
    if index:
        df.index = index
    df.index.name = index_name


def run_pca(m, k=2):
    return PCA(n_components=k).fit_transform(m)


def run_ica(m, k=2):
    return FastICA(n_components=k).fit_transform(m)


def run_nmf(m, k=2):
    return NMF(n_components=k).fit_transform(m)


# manifold embedding


def run_tsne(m, perplexity=30):
    return TSNE(n_components=2, init='pca', random_state=0, perplexity=perplexity).fit_transform(m)


def run_umap(m):
    return UMAP().fit_transform(m)


def run_phate(m, k=2):
    return PHATE(n_components=k).fit_transform(m)


def run_spectral(m, k=2):
    return SpectralEmbedding(n_conponents=k).fit_transform(m)


def run_mds(m, k=2):
    return MDS(n_components=k).fit_transform(m)


def run_isomap(m, k=2):
    return Isomap(n_components=k).fit_transform(m)


def run_diffusion(m, k=2):
    return DiffusionMap.from_sklearn(n_evecs=k).fit_transform(m)


def run_lle(m, k=2):
    return LocallyLinearEmbedding(n_components=k, method='standard')


def run_ltsa(m, k=2):
    return LocallyLinearEmbedding(n_components=k, method='ltsa')


def run_hessian_lle(m, k=2):
    return LocallyLinearEmbedding(n_components=k, method='hessian')


def run_modified_lle(m, k=2):
    return LocallyLinearEmbedding(n_components=k, method='modified')
