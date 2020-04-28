# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 00:45:26 2017

@author: marcos
"""

import numpy as np
import pandas as pd

# set working directory
import os
import sys
root_path = "./../../main/"
os.chdir(root_path)

sys.path.append(os.getcwd())

from borda import evaluation as borda
from datetime import datetime
from execution import selection as feat_selection
from helpers import logger, time
from data.reader import DataReader
import common.presets as presets
from common.presets import FoldersLocation
from common.presets import BordaCombinations
import execution.initialization as init

result_col_names = presets.get_result_column_names()
dataSets = presets.get_datasets_names()
methods = presets.get_methods_names()


def run():
    result = pd.DataFrame(columns=result_col_names)

    # variance_thresholds = [1, 0.25, 0.50, 0.75]
    variance_thresholds = [1]

    # combinations = list(itertools.combinations([1, 2], 2))

    # borda combinations
    # combinations = []
    combinations = [BordaCombinations.LS_SPEC,
                    BordaCombinations.LS_IDETECT,
                    BordaCombinations.LS_SPEC_IDETECT,
                    BordaCombinations.SPEC_IDETECT,
                    BordaCombinations.GLSPFS_LS,
                    BordaCombinations.GLSPFS_SPEC,
                    BordaCombinations.GLSPFS_IDETECT,
                    BordaCombinations.GLSPFS_LS_SPEC,
                    BordaCombinations.GLSPFS_LS_IDETECT,
                    BordaCombinations.GLSPFS_SPEC_IDETECT,
                    BordaCombinations.GLSPFS_LS_SPEC_IDETECT]

    for variance_threshold in variance_thresholds:

        for dataset_name in dataSets:

            reader = DataReader(dataset_name)

            time.start_time()

            dataset, n_features, y_true = reader.get_preprocessed_data()

            time.end_time("read dataset")

            # default_values = state of art
            control = init.get_initial_variables(is_default_values=False)

            rankings = np.zeros([n_features, 1])

            for method in methods:

                control.best_silhouette = 0

                current_result, best_rank = feat_selection.run_and_evaluate_fs_methods(dataset,
                                                                                       dataset_name,
                                                                                       method,
                                                                                       y_true,
                                                                                       result_col_names,
                                                                                       variance_threshold,
                                                                                       control)

                result = pd.concat([result, current_result])
                results_filename = "result_best_fs_" + dataset_name + ".csv"
                result.to_csv(FoldersLocation.results.value + results_filename, sep=" ")

                rank = pd.Series(best_rank)
                logger.log("best rank: " + str(rank.shape), False)

                rankings = np.append(rankings, rank[:, None], 1)

            # Adding Borda Count results
            if not control.state_of_art:
                for comb in combinations:
                    borda_results = borda.get_borda_results(rankings,
                                                            dataset,
                                                            dataset_name,
                                                            result_col_names,
                                                            y_true,
                                                            combination=comb)
                    result = pd.concat([result, borda_results])
            variance_results_filename = "result_after_" + str(variance_threshold) + "_variance_best_fs_" + dataset_name + ".csv"
            results_filename = FoldersLocation.results.value + variance_results_filename
            result.to_csv(results_filename, sep=" ")

# cuda.select_device(0)
# print(cuda.gpus)
dt_1 = datetime.now()

run()

dt_2 = datetime.now()
total_time = dt_2 - dt_1
logger.log("total time elapsed: " + str(total_time), True)

#result = pd.concat([result_from_LS])


"""
if __name__ == '__main__':
    main()
"""
