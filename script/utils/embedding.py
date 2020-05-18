#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Embedding Map
'''

import pandas as pd
from sklearn.decomposition import PCA, FastICA, NMF
from sklearn.manifold import TSNE
from umap import UMAP
from phate import PHATE


def get_phate(m, index=None, index_name='index'):
    df = pd.DataFrame(PHATE().fit_transform(m), columns=['e_PHATE1', 'e_PHATE2'])
    if index:
        df.index = index
    df.index.name = index_name
    return df


def get_pca(m, index=None, index_name='index'):
    df = pd.DataFrame(PCA(n_components=2).fit_transform(m), columns=['e_PC1', 'e_PC2'])
    if index:
        df.index = index
    df.index.name = index_name
    return df


def get_ica(m, index=None, index_name='index'):
    df = pd.DataFrame(FastICA(n_components=2).fit_transform(m), columns=['e_ICA1', 'e_CIA2'])
    if index:
        df.index = index
    df.index.name = index_name
    return df


def get_nmf(m, index=None, index_name='index'):
    df = pd.DataFrame(NMF(n_components=2).fit_transform(m), columns=['e_NMF1', 'e_NMF2'])
    if index:
        df.index = index
    df.index.name = index_name
    return df


def get_tsne(m, index=None, index_name='index', perplexity=30):
    df = pd.DataFrame(TSNE(n_components=2).fit_transform(m), columns=['e_TSNE1', 'e_TSNE2'])
    if index:
        df.index = index
    df.index.name = index_name
    return df


def get_umap(m, index=None, index_name='index'):
    df = pd.DataFrame(UMAP().fit_transform(m), columns=['e_UMAP1', 'e_UMAP2'])
    if index:
        df.index = index

    df.index.name = index_name
    return df
