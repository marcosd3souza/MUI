def mount_partial_result(dataset_name, n_features, method, cutoff_method, cut_point, clustering_result):
    return [dataset_name,  # 0
            n_features,  # 1
            method,  # 2
            cutoff_method,  # 3
            cut_point,  # 4
            clustering_result.inertia,  # 5
            clustering_result.inertia / cut_point,  # 6
            clustering_result.avg_sil,  # 7
            clustering_result.dunn,  # 8
            clustering_result.dunn2,  # 9
            clustering_result.entropy,  # 10
            clustering_result.ch,  # 11
            clustering_result.nmi,  # 12
            clustering_result.acc,  # 13
            clustering_result.corrected_rand,  # 14
            clustering_result.f_measure]  # 15


def get_column_names():
    return ["dataset_name",
            "n_features",
            "method",
            "cutoff_method",
            "cut_point",
            "inertia",
            "inertia / cut_point",
            "avg_sil",
            "dunn",
            "dunn2",
            "entropy",
            "ch",
            "nmi",
            "acc",
            "corrected_rand",
            "f_measure"]
