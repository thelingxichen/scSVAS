

from sklearn.cluster import SpectralClustering
import numpy as np

def spectral_clustering(X, k):
    label = SpectralClustering(n_clusters=k,
            assign_labels="discretize",
            random_state=0).fit_predict(X)
    return label
