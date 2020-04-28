# -*- coding: utf-8 -*-
from common.commons import get_cutoff_magic_numbers
from helpers import logger
from evaluation import unsupervised
from helpers.logger import mount_beauty_output


def evaluate(features, dataset, y, dataset_name, combination_name):
    # cutoff_methods = ['all_features']
    n_features = dataset.shape[1]
    
    result = []

    best_nmi = 0
    max_nmi = 0
    max_corrected_rand = 0
    max_acc = 0
    best_corrected_rand = 0
    best_acc = 0
    best_f_measure = 0
    best_cutoff_method = ""
    best_cutoff_point = 0
    best_inertia = 0
    best_avg_sil = 0
    number_of_clusters = 0

    # partial_result = []
    
    cutoff_methods = get_cutoff_magic_numbers()

    for cutoff_method in cutoff_methods:

        cut_point = cutoff_method

        if cut_point >= 3:
            logger.log("verify cut_off " + str(cutoff_method) + " from method: " + combination_name, False)
            features_selected = features[0: cut_point]
            dataset_filtered = dataset.iloc[:, features_selected]

            clustering_result = unsupervised.evaluation(x_selected=dataset_filtered.values, y=y)

            if clustering_result.nmi > max_nmi:
                max_nmi = clustering_result.nmi

            if clustering_result.acc > max_acc:
                max_acc = clustering_result.acc

            if clustering_result.corrected_rand > max_corrected_rand:
                max_corrected_rand = clustering_result.corrected_rand

            # analysis about partial result
            """
            current_result = mount_partial_result(dataset_name,
                                                  n_features,
                                                  combination_name,
                                                  cutoff_method,
                                                  cut_point,
                                                  clustering_result)
            
            partial_result.append(current_result)
            """

            if clustering_result.avg_sil > best_avg_sil or best_avg_sil == 0:

                best_avg_sil = clustering_result.avg_sil
                number_of_clusters = clustering_result.number_of_clusters

                best_inertia = clustering_result.inertia
                best_nmi = clustering_result.nmi
                best_corrected_rand = clustering_result.corrected_rand
                best_cutoff_method = cutoff_method
                best_cutoff_point = cut_point
                best_f_measure = clustering_result.f_measure
                best_acc = clustering_result.acc

                dataset_filtered.to_csv("../results/" + dataset_name + "_after_FS_" + combination_name + ".csv", sep=" ")

    mount_beauty_output(dataset_name, best_avg_sil, combination_name, best_nmi, max_nmi, best_acc, max_acc)

    result.append(
        [number_of_clusters, 'Borda', dataset_name, n_features, combination_name, best_cutoff_method, best_cutoff_point,
         best_inertia, best_avg_sil,
         best_nmi, max_nmi, best_acc, max_acc, best_corrected_rand, max_corrected_rand, best_f_measure])

    return result
