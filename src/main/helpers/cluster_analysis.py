# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
from sklearn import metrics
import pandas as pd

from helpers import logger
from helpers.scores_cutoff import get_cut_off_point_by_second_derivate


def get_number_of_clusters(dataset):
    cluster_range = range(2, 21)
    silhouettes = []

    logger.log("Defining number of clusters ...", True)

    for num_clusters in cluster_range:
        model = KMeans(n_clusters=num_clusters, init='k-means++', n_init=50, max_iter=300,
                       tol=0.001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=-1)

        model.fit(dataset)

        silhouettes.append(metrics.silhouette_score(dataset, model.labels_, metric='euclidean'))

    number = get_cut_off_point_by_second_derivate(pd.DataFrame(silhouettes)) - 2
    logger.log("selected: " + str(number) + " clusters", True)

    return number


