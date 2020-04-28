import threading
import warnings

import numpy as np
from scipy.optimize import linear_sum_assignment as la
# from numba import jit
from numba import jit
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics.cluster import v_measure_score
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import f1_score
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold
from multiprocessing import Pool
import functools
# from rpy2.robjects.packages import importr
# import rpy2.robjects as robjects
# from rpy2.robjects import pandas2ri
# import rpy2.robjects.numpy2ri

from models.evaluation_results import ClusteringResults
from helpers import logger, time
import pandas as pd
from sklearn import metrics
from scipy.spatial.distance import cdist

# rpy2.robjects.numpy2ri.activate()

# pip install rpy2
# r = robjects.r
# fpc = importr('fpc')
# factoextra = importr('factoextra')
# stats = importr('stats')
from helpers.scores_cutoff import get_cut_off_point_by_second_derivate, get_point_by_inflexion


def best_map(l1, l2):
    """
    Permute labels of l2 to match l1 as much as possible
    """
    if len(l1) != len(l2):
        print("L1.shape must == L2.shape")
        exit(0)

    label1 = np.unique(l1)
    n_class1 = len(label1)

    label2 = np.unique(l2)
    n_class2 = len(label2)

    n_class = max(n_class1, n_class2)
    G = np.zeros((n_class, n_class))

    for i in range(0, n_class1):
        for j in range(0, n_class2):
            ss = l1 == label1[i]
            tt = l2 == label2[j]
            G[i, j] = np.count_nonzero(ss & tt)

    A = la(-G)

    new_l2 = np.zeros(l2.shape)
    for i in range(0, n_class2):
        new_l2[l2 == label2[A[i][1]]] = label1[A[i][0]]
    return new_l2.astype(int)


def evaluation(x_selected, y, state_of_art=False):
    """
    This function calculates ARI, ACC and NMI of clustering results

    Input
    -----
    X_selected: {numpy array}, shape (n_samples, n_selected_features}
            input data on the selected features
    n_clusters: {int}
            number of clusters
    y: {numpy array}, shape (n_samples,)
            true labels

    Output
    ------
    nmi: {float}
        Normalized Mutual Information
    acc: {float}
        Accuracy
    """
    # check_number_of_clusters(X_selected)
    # n_clusters = best_number_of_clusters

    y_true = np.asarray(y)

    if state_of_art:
        avg_sil, model = get_results(x_selected, [max(y_true)])
    else:
        avg_sil, model = get_results(x_selected)

    # using GPU
    #avg_sil, model = get_results_from_GPU(x_selected)

    """ VALID DISTANCES METRICS
    'euclidean', 'l2', 'l1', 'manhattan', 'cityblock',
    'braycurtis', 'canberra', 'chebyshev', 'correlation',
    'cosine', 'dice', 'hamming', 'jaccard', 'kulsinski',
    'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto',
    'russellrao', 'seuclidean', 'sokalmichener',
    'sokalsneath', 'sqeuclidean', 'yule', "wminkowski"
    
     max([
           metrics.silhouette_score(x_selected, model.labels_, metric='euclidean'),
           metrics.silhouette_score(x_selected, model.labels_, metric='cosine'),

           metrics.silhouette_score(x_selected, model.labels_, metric='manhattan'),
           metrics.silhouette_score(x_selected, model.labels_, metric='braycurtis'),
           metrics.silhouette_score(x_selected, model.labels_, metric='canberra'),
           metrics.silhouette_score(x_selected, model.labels_, metric='chebyshev'),
           metrics.silhouette_score(x_selected, model.labels_, metric='hamming'),
           metrics.silhouette_score(x_selected, model.labels_, metric='jaccard'),

           metrics.silhouette_score(x_selected, model.labels_, metric='russellrao'),
           metrics.silhouette_score(x_selected, model.labels_, metric='sokalsneath'),
           metrics.silhouette_score(x_selected, model.labels_, metric='yule'),

           metrics.silhouette_score(x_selected, model.labels_, metric='kulsinski'),
           metrics.silhouette_score(x_selected, model.labels_, metric='cityblock')
           ])"""

    y_predict = model.labels_

    for i in range(0, len(y_predict)):
        y_predict[i] = y_predict[i] + 1

    # inercia = k_means.inertia_
    inertia = model.inertia_

    # calculate NMI
    nmi = v_measure_score(y_true, y_predict)
    # nmi = 0

    # calculate corrected rand
    corrected_rand = adjusted_rand_score(y_true, y_predict)
    # corrected_rand = 0

    # calculate f-measure
    f_measure = f1_score(y_true, y_predict, average='micro')

    # calculate ACC

    label1 = np.unique(y_true)
    label2 = np.unique(y_predict)
    if len(label1) == len(label2):
        y_permuted_predict = best_map(y_true, y_predict)
        acc = accuracy_score(y_true, y_permuted_predict)
    else:
        acc = 0

    logger.log("KMeans model has"
               " avg_sil = " + str(avg_sil) +
               " and NMI = " + str(nmi) +
               " and CR = " + str(corrected_rand) +
               " and f-measure = " + str(f_measure), True)

    # calculate cluster.stats
    # dgene = stats.dist(x_selected, method='euclidean')

    """ fpc_result = fpc.cluster_stats(dgene,
                                   model.labels_,
                                   G2=False,
                                   G3=False,
                                   silhouette=True,
                                   sepwithnoise=True,
                                   noisecluster=True,
                                   wgap=True)

    stats_fpc = pandas2ri.ri2py(fpc_result)"""

    # Compute Hopkins statistic for iris dataset
    # nrow = X_selected.shape[0]
    # res = factoextra.get_clust_tendency(X_selected, n=nrow - 1, graph=False)
    # print("hopkins test: "+ str(res[0]))
    # hopkins_test = res

    # dunn = stats_fpc[24][0]
    # dunn2 = stats_fpc[25][0]
    # entropy = stats_fpc[26][0]
    # ch = stats_fpc[28][0]

    dunn = 0
    dunn2 = 0
    entropy = 0
    ch = 0

    # inertia, avg_sil, dunn, dunn2, entropy, ch, nmi, acc, corrected_rand, f_measure
    return ClusteringResults(max(y_predict), inertia, avg_sil, dunn, dunn2, entropy, ch, nmi, acc, corrected_rand, f_measure)


def get_results(x_selected, number_of_clusters=None):

    if number_of_clusters is None:
        best_number_of_clusters = get_k_by_gap_statistic(x_selected)
    else:
        best_number_of_clusters = number_of_clusters

    logger.log("Number of clusters: " + str(best_number_of_clusters), True)

    return get_avg_sil(x_selected, best_number_of_clusters)


def get_avg_sil(x_selected, n_clusters):
    model = get_model(x_selected, n_clusters)

    # avg_sil = metrics.silhouette_score(x_selected, model.labels_, metric='euclidean')

    # usando o min evita que seja influenciado pela medida de distancia
    # ex.:
    # se a silhueta para as medidas euclideana, manhatan e hammig forem 0.3; 0.6; 0.2
    # ao utilizar o maior (manhatan 0.6) estariamos mascarando que houve uma silhueta de 0.2
    # assim podemos assumir uma "boa" silhueta quando consideramos um minimo local
    # avg_sil = metrics.silhouette_score(x_selected, model.labels_, metric='euclidean')
    avg_sil = np.average([
           metrics.silhouette_score(x_selected, model.labels_, metric='euclidean'),
           metrics.silhouette_score(x_selected, model.labels_, metric='cosine'),
           metrics.silhouette_score(x_selected, model.labels_, metric='manhattan')

            #metrics.silhouette_score(x_selected, model.labels_, metric='braycurtis'),
            #metrics.silhouette_score(x_selected, model.labels_, metric='canberra'),
            #metrics.silhouette_score(x_selected, model.labels_, metric='chebyshev'),
            #metrics.silhouette_score(x_selected, model.labels_, metric='hamming'),
            # metrics.silhouette_score(x_selected, model.labels_, metric='jaccard'),

            #  metrics.silhouette_score(x_selected, model.labels_, metric='russellrao'),
            #  metrics.silhouette_score(x_selected, model.labels_, metric='sokalsneath'),
            #  metrics.silhouette_score(x_selected, model.labels_, metric='yule'),
            #  metrics.silhouette_score(x_selected, model.labels_, metric='kulsinski'),
           # metrics.silhouette_score(x_selected, model.labels_, metric='cityblock')
           ])

    return avg_sil, model


def get_model(x_selected, n_clusters):
    model = KMeans(n_clusters=n_clusters, init='k-means++', n_init=30,
                   precompute_distances=True, verbose=0, copy_x=True, n_jobs=-1)

    return model.fit(x_selected)


def get_k_by_gap_statistic(data, nrefs=5):
    """
    Calculates KMeans optimal K using Gap Statistic from Tibshirani, Walther, Hastie
    Params:
        data: ndarry of shape (n_samples, n_features)
        nrefs: number of sample reference preprocessed_datasets to create
        maxClusters: Maximum number of clusters to test for
    Returns: (gaps, optimalK)
    """

    number_of_clusters = range(2, 15)

    gaps = np.zeros((len(number_of_clusters),))

    for gap_index, k in enumerate(number_of_clusters):

        # Holder for reference dispersion results
        ref_disps = np.zeros(nrefs)

        # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            # Create new random reference set
            random_reference = np.random.random_sample(size=data.shape)

            # Fit to it
            km = KMeans(n_clusters=k, init='k-means++', n_init=30,
                        precompute_distances=True, verbose=0, copy_x=True, n_jobs=-1)
            km.fit(random_reference)

            ref_disp = km.inertia_
            ref_disps[i] = ref_disp

        # Fit cluster to original data and create dispersion
        km = KMeans(n_clusters=k, init='k-means++', n_init=30,
                    precompute_distances=True, verbose=0, copy_x=True, n_jobs=-1)
        km.fit(data)

        orig_disp = km.inertia_

        # Calculate gap statistic
        gap = np.log(np.mean(ref_disps)) - np.log(orig_disp)

        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap

    # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal
    return gaps.argmax() + 1
