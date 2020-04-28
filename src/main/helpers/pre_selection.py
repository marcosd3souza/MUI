from scipy.stats.stats import pearsonr
import pandas as pd
from sklearn.feature_selection.variance_threshold import VarianceThreshold

# remove redundant Features
def apply_pearson_filter(dataset, dataset_name, n_features):

    print("total fea before correlation filter: " + str(n_features))

    features_to_remove = []

    for i in range(0, n_features - 1):
        a = list(dataset.iloc[:, i])

        for j in range(i + 1, n_features - 1):
            b = list(dataset.iloc[:, j])

            if abs(round(pearsonr(a, b)[0], 3)) >= 0.985 and a != b:
                print("pearson cor: " + str(abs(round(pearsonr(a, b)[0], 3))) +
                      " a: " + str(dataset.columns[i]) + " b: " + str(dataset.columns[j]))
                if str(dataset.columns[j]) not in features_to_remove:
                    features_to_remove.append(str(dataset.columns[j]))

    dataset = dataset.drop(features_to_remove, axis=1)

    return dataset


def apply_variance_filter(dataset, variance_threshold):
    print("dataset before variance filter: " + str(dataset.shape))

    if variance_threshold != 1:
        cut_point = round(variance_threshold * dataset.shape[1])

        variances = dataset.var()
        data = pd.DataFrame({"variance": variances, "feature": dataset.columns.values})
        data_sorted = data.sort_values(by="variance", ascending=False)

        data_filtered = data_sorted.iloc[0:int(cut_point), :]
        dataset = dataset.loc[:, data_filtered.loc[:, "feature"].values]

    print("dataset after variance filter: " + str(dataset.shape))

    return dataset
