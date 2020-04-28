import pandas as pd
from helpers import normalize, logger
from helpers.pre_selection import apply_variance_filter


class DataReader:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.dataset_folder = "/media/marcos/DATA/datasets"
        self.preprocessed_data_folder = "/preprocessed/"
        self.raw_data_folder = "/raw/"

    def get_preprocessed_data(self):
        # original preprocessed_datasets
        dataset_folder_file_name = self.dataset_folder + self.preprocessed_data_folder

        dataset_file_name = dataset_folder_file_name + self.dataset_name + ".csv"

        dataset = pd.read_csv(dataset_file_name, index_col=False, sep=" ")

        y = list(dataset.loc[:, 'Y'])
        dataset = dataset.drop(['Y'], axis=1)

        # get normalized data
        data_transposed = dataset.T
        dataset = normalize.get_normalized_data(data_transposed).T

        logger.log("reading dataset " + self.dataset_name + " with shape " + str(dataset.shape), True)

        n_features = dataset.shape[1]

        return dataset, n_features, y