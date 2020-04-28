from scipy.stats.stats import pearsonr
import numpy as np
from enum import Enum


class Cutoff(Enum):
    ALL_FEA = -1
    INFLEXION_BY_SILHOUETTE = 0
    INFLEXION = 1
    PERCENT_25 = 2
    PERCENT_45 = 3
    PERCENT_65 = 4
    PERCENT_85 = 5
    QUARTILE_1 = 6
    QUARTILE_2 = 7
    QUARTILE_3 = 8


def get_cutoff_magic_numbers():
    """
    initial_number_of_features = 10
    top_scores = [initial_number_of_features]
    for factor in range(100, 10, -5):
        last_top = top_scores[len(top_scores) - 1]
        top = int(last_top + (0.01 * factor) * last_top)

        if top > n_features or top >= 350:
            break

        top_scores.append(top)

    return top_scores
    """
    return range(10, 310, 10)


def remove_duplicated_rankings(scores):
    cols_to_remove = []
    scores = np.delete(scores, 0, 1)

    for i in range(0, scores.shape[1] - 1):
        a = scores[:, i]
        for j in range(1, scores.shape[1]):
            b = scores[:, j]

            if pearsonr(a, b)[0] == 1.0 and j > i and j not in cols_to_remove:
                cols_to_remove.append(j)

    scores = np.delete(scores, cols_to_remove, 1)

    return scores

