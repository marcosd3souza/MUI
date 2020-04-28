# -*- coding: utf-8 -*-
from numba import jit

from common import methods_chooser as cs
from common.commons import Cutoff
import common.results as res
from common.presets import FoldersLocation as foldersLocation
from helpers import logger, scores_cutoff as cutoff, time
from evaluation import unsupervised
import pandas as pd
from helpers.logger import mount_beauty_output

n_features = 0


#@jit
def run_and_evaluate_fs_methods(dataset, dataset_name, method, y, cols, variance_threshold, control):
    logger.log("dataset after: " + str(dataset.shape), False)

    global n_features
    n_features = dataset.shape[1]

    best_nmi = control.initial_best_metric
    max_nmi = control.initial_best_metric
    max_acc = control.initial_best_metric
    max_corrected_rand = control.initial_best_metric
    best_corrected_rand = control.initial_best_metric
    best_acc = control.initial_best_metric
    best_f_measure = control.initial_best_metric
    best_cutoff_point = control.initial_best_metric
    best_inertia = control.initial_best_metric
    number_of_clusters = 0

    all_opt_to_save = pd.DataFrame()

    result = []
    best_ranking = []

    all_method_config_ranks = run_fs_method(method, dataset, control.state_of_art)
    count_configs = all_method_config_ranks.shape[1]

    for config in range(0, count_configs):

        partial_result = []
        cutoff_options_list = pd.DataFrame()

        logger.log("evaluate " + method + " setting " + str(config + 1) + " of " + str(count_configs), True)

        scores = all_method_config_ranks[:, config]
        scores_df = pd.DataFrame({"feature": range(0, n_features), "score": scores})
        scores_sorted = scores_df.sort_values(by="score", ascending=False)

        scores_values = pd.DataFrame(scores_sorted.iloc[:, 1])
        scores_values.reset_index(drop=True, inplace=True)

        logger.log("total sum of scores: " + str(sum(scores_values.values)), False)

        logger.log("total cutoff methods: " + str(len(control.cutoff_methods)), False)

        for cutoff_method in control.cutoff_methods:

            cut_point = get_cut_point(cutoff_method, scores_values)

            if cut_point == Cutoff.INFLEXION_BY_SILHOUETTE.name or (3 <= cut_point < n_features):

                features_selected = scores_sorted.iloc[0:cut_point, 0]
                dataset_reduced = dataset.iloc[:, features_selected]

                logger.log(
                    "verify cut_off " + str(cutoff_method) + " from method: " + method + " config n:" + str(config),
                    False)

                time.start_time()

                clustering_result = unsupervised.evaluation(x_selected=dataset_reduced.values, y=y, state_of_art=control.state_of_art)

                time.end_time("evaluate the model", False)

                current_cutoff_result_df = pd.DataFrame({
                    "pos": [cut_point],
                    "values": [clustering_result.avg_sil],
                    "cut_method": [cutoff_method],
                    "cut_point": [cut_point],
                    "clustering_result": [clustering_result]
                })

                cutoff_options_list = cutoff_options_list.append(current_cutoff_result_df)

                current_result = res.mount_partial_result(dataset_name,
                                                          n_features,
                                                          method,
                                                          cutoff_method,
                                                          cut_point,
                                                          clustering_result)

                partial_result.append(current_result)

                if clustering_result.nmi > max_nmi:
                    max_nmi = clustering_result.nmi

                if clustering_result.acc > max_acc:
                    max_acc = clustering_result.acc

                if clustering_result.corrected_rand > max_corrected_rand:
                    max_corrected_rand = clustering_result.corrected_rand

        # best_cutoff_point = get_point_by_inflexion(pd.DataFrame(cutoff_options_list.loc[:, "values"]))

        best_option = pd.DataFrame(cutoff_options_list.sort_values(by="values", ascending=False).iloc[0, :])

        clustering_result = best_option.loc["clustering_result", :][0]
        cut_point = best_option.loc["cut_point", :][0]
        best_cutoff_method = best_option.loc["cut_method", :][0]

        features_selected = scores_sorted.iloc[0:cut_point, 0]
        dataset_reduced = dataset.iloc[:, features_selected]

        partial_result_to_save = pd.DataFrame(partial_result, columns=res.get_column_names())
        all_opt_to_save = pd.concat([all_opt_to_save, partial_result_to_save])

        logger.log("\n\n<------------------------------------------------->\n" +
                   "The config (higher silhouette) has :" +
                   "\navg_sil: " + str(clustering_result.avg_sil) +
                   "\nnmi: " + str(clustering_result.nmi) +
                   "\n<--------------------------------------------------->\n\n"
                   , False)

        if clustering_result.avg_sil > control.best_silhouette:
            control.best_silhouette = clustering_result.avg_sil

            best_ranking = scores_sorted.loc[:, 'feature'].tolist()

            number_of_clusters = clustering_result.number_of_clusters

            best_inertia = clustering_result.inertia # current_result[5]
            best_nmi = clustering_result.nmi # current_result[12]
            best_corrected_rand = clustering_result.corrected_rand # current_result[14]
            control.best_cutoff_method = best_cutoff_method # current_result[3]
            best_cutoff_point = cut_point # current_result[4]
            best_f_measure = clustering_result.f_measure # current_result[15]
            best_acc = clustering_result.acc # current_result[13]
            control.best_config = config

            dataset_reduced.to_csv(foldersLocation.results.value + dataset_name + "_after_FS_" + method + ".csv", sep=" ")

    result.append([number_of_clusters, control.best_config, dataset_name, n_features, method, control.best_cutoff_method, best_cutoff_point, best_inertia,
                   control.best_silhouette, best_nmi, max_nmi, best_acc, max_acc, best_corrected_rand, max_corrected_rand,
                   best_f_measure])

    result = pd.DataFrame(result, columns=cols)

    result = result.sort_values(by="best_avg_sil", ascending=False)

    result = pd.DataFrame(result.iloc[0, :]).T

    all_opt_to_save.to_csv(foldersLocation.results.value + "result_all_opt_" + method + "_in_" + dataset_name + ".csv", sep=" ")

    mount_beauty_output(dataset_name, control.best_silhouette, method, best_nmi, max_nmi, best_acc, max_acc)

    # rankings = best_ranking
    # config_cols = ["config", "ranking"]
    # rankings = pd.DataFrame(rankings, columns=config_cols)
    # best_ranking = rankings.loc[rankings['config'] == result.iloc[0, 0], 'ranking'].tolist()[0]

    return result, best_ranking


def run_fs_method(method, dataset, default_method_configs):
    if method == 'iDetect':
        numpy_data = dataset.values
        all_configs_by_method = cs.run_method(numpy_data.T, method, default_method_configs)
    else:
        numpy_data = dataset.values
        all_configs_by_method = cs.run_method(numpy_data, method, default_method_configs)

    return all_configs_by_method


def get_cut_point(cutoff_method, values):
    if cutoff_method == Cutoff.INFLEXION.name:
        cut_point = cutoff.get_cut_off_point_by_second_derivate(values, 4)
    elif cutoff_method == Cutoff.QUARTILE_1.name:
        cut_point = cutoff.get_cut_off_point_by_quartile(values, 1)
    elif cutoff_method == Cutoff.QUARTILE_2.name:
        cut_point = cutoff.get_cut_off_point_by_quartile(values, 2)
    elif cutoff_method == Cutoff.QUARTILE_3.name:
        cut_point = cutoff.get_cut_off_point_by_quartile(values, 3)
    elif cutoff_method == Cutoff.PERCENT_25.name:
        cut_point = cutoff.get_cut_off_point_by_percent(values, 0.25)
    elif cutoff_method == Cutoff.PERCENT_45.name:
        cut_point = cutoff.get_cut_off_point_by_percent(values, 0.45)
    elif cutoff_method == Cutoff.PERCENT_65.name:
        cut_point = cutoff.get_cut_off_point_by_percent(values, 0.65)
    elif cutoff_method == Cutoff.PERCENT_85.name:
        cut_point = cutoff.get_cut_off_point_by_percent(values, 0.85)
    elif cutoff_method == Cutoff.ALL_FEA.name:
        cut_point = n_features
    else:
        cut_point = cutoff_method

    return cut_point

