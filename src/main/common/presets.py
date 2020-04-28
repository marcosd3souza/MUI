
from enum import Enum


class FoldersLocation(Enum):
    preprocessed_datasets = "/media/marcos/DATA/datasets/preprocessed_datasets/"
    results = "../../data/output/"


class BordaCombinations(Enum):
    LS_SPEC = 0
    LS_IDETECT = 1
    SPEC_IDETECT = 2
    LS_SPEC_IDETECT = 3
    GLSPFS_LS = 4
    GLSPFS_SPEC = 5
    GLSPFS_IDETECT = 6
    GLSPFS_LS_SPEC = 7
    GLSPFS_LS_IDETECT = 8
    GLSPFS_SPEC_IDETECT = 9
    GLSPFS_LS_SPEC_IDETECT = 10


def get_result_column_names():
    return ["selected_K", "config", "dataset", "total_features",  "method_FS", "Method_cut", "selected_features",
            "inercia", "best_avg_sil",  "nmi", "max_nmi", "acc", "max_acc", "corrected_rand", "max_corrected_rand",
            "f_measure"]


def get_datasets_names(filter=None):
    available_datasets = ["warpAR10P", "warpPIE10P", "ALLAML", "Carcinom", "ProstateGE", "TOX171", "pixraw10P", "SMK_CAN", "PCMAC", "BASEHOCK", "RELATHE"]
    result = []

    if filter is not None and len(filter) > 0:
        for i in filter:
            result.append(available_datasets[i-1])
        return result
    else:
        return available_datasets


def get_methods_names(filter=None):
    # available_methods = ["LS", "SPEC", "iDetect", "GLSPFS"]
    available_methods = ["GLSPFS"]
    result = []

    if filter is not None and len(filter) > 0:
        for i in filter:
            result.append(available_methods[i-1])
        return result
    else:
        return available_methods

