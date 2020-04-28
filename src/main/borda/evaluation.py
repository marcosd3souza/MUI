from evaluation import rankings
from borda import borda_count
from common.presets import BordaCombinations
import pandas as pd

n_clusters = -1


def merge_rankings(rankings, positions, dataset, name, label_name, y, cols):
    merged_ranks = []

    if len(positions) == 2:
        merged_ranks = borda_count.borda_sort([rankings[:, positions[0]], rankings[:, positions[1]]])
    elif len(positions) == 3:
        merged_ranks = borda_count.borda_sort([rankings[:, positions[0]], rankings[:, positions[1]],
                                               rankings[:, positions[2]]])
    elif len(positions) == 4:
        merged_ranks = borda_count.borda_sort([rankings[:, positions[0]], rankings[:, positions[1]],
                                               rankings[:, positions[2]], rankings[:, positions[3]]])

    result = evaluate_borda(merged_ranks, dataset, name, label_name, y, cols)
    return pd.DataFrame(result)


def evaluate_borda(merged_ranks, dataset, dataset_name, label, y, cols):

    result_borda = rankings.evaluate(merged_ranks, dataset, y, dataset_name, label)

    result_tb = pd.DataFrame(result_borda, columns=cols)

    return result_tb


def get_borda_results(rankings, dataset, dataset_name, cols, y, combination):
    result = pd.DataFrame(columns=cols)

    # LS - SPEC
    if combination == BordaCombinations.LS_SPEC:
        result = pd.concat([result, merge_rankings(rankings, [1, 2], dataset, dataset_name, 'Borda_LS_SPEC', y, cols)])

    # LS - iDetect
    if combination == BordaCombinations.LS_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [1, 3], dataset, dataset_name, 'Borda_LS_iDetect', y, cols)])

    # SPEC - iDetect
    if combination == BordaCombinations.SPEC_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [2, 3], dataset, dataset_name, 'Borda_SPEC_iDetect', y, cols)])

    # LS - SPEC - iDetect
    if combination == BordaCombinations.LS_SPEC_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [1, 2, 3], dataset, dataset_name, 'Borda_LS_SPEC_iDetect', y, cols)])

    # LS - GLSPFS
    if combination == BordaCombinations.GLSPFS_LS:
        result = pd.concat([result, merge_rankings(rankings, [1, 4], dataset, dataset_name, 'Borda_LS_GLSPFS', y, cols)])

    # LS - SPEC - GLSPFS
    if combination == BordaCombinations.GLSPFS_LS_SPEC:
        result = pd.concat(
            [result, merge_rankings(rankings, [1, 2, 4], dataset, dataset_name, 'Borda_LS_SPEC_GLSPFS', y, cols)])

    # LS - iDetect - GLSPFS
    if combination == BordaCombinations.GLSPFS_LS_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [1, 3, 4], dataset, dataset_name, 'Borda_LS_iDetect_GLSPFS', y, cols)])

    # SPEC - GLSPFS
    if combination == BordaCombinations.GLSPFS_SPEC:
        result = pd.concat(
            [result, merge_rankings(rankings, [2, 4], dataset, dataset_name, 'Borda_SPEC_GLSPFS', y, cols)])

    # SPEC - iDetect - GLSPFS
    if combination == BordaCombinations.GLSPFS_SPEC_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [2, 3, 4], dataset, dataset_name, 'Borda_SPEC_iDetect_GLSPFS', y, cols)])

    # iDetect - GLSPFS
    if combination == BordaCombinations.GLSPFS_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [3, 4], dataset, dataset_name, 'Borda_iDetect_GLSPFS', y, cols)])

    # LS - SPEC - iDetect - GLSPFS
    if combination == BordaCombinations.GLSPFS_LS_SPEC_IDETECT:
        result = pd.concat([result, merge_rankings(rankings, [1, 2, 3, 4], dataset, dataset_name,
                                                   'Borda_LS_SPEC_iDetect_GLSPFS', y, cols)])

    return result
