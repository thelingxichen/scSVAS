#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Embedding Map 
'''

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP 


def get_pca(m, index, index_name):
    df = pd.DataFrame(PCA(n_components=2).fit_transform(m), columns=['e_PC1', 'e_PC2'], index=index)
    df.index.name = index_name
    return df 


def get_tsne(m, index, index_name, perplexity=30):
    df = pd.DataFrame(TSNE(n_components=2).fit_transform(m), columns=['e_TSNE1', 'e_TSNE2'], index=index)
    df.index.name = index_name
    return df


def get_umap(m, index, index_name):
    df = pd.DataFrame(UMAP().fit_transform(m), columns=['e_UMAP1', 'e_UMAP2'], index=index)
    df.index.name = index_name
    return df
