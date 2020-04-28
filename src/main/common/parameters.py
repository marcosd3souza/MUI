# -*- coding: utf-8 -*-

import math
import numpy as np


# to build kernel params use the default values:
# p1Candidates = {'Linear', 'PolyPlus', 'Polynomial', 'Gaussian'};
# p2Candidates = {[], [2, 4], [2, 4], [0.01, 0.05, 0.1, 1, 10, 50, 100]};
# p3Candidates = {'Sample-Scale'};
def get_GLSPFS_kernel_options():
    options = []
    p1_candidates = ["Linear", "PolyPlus", "Polynomial", "Gaussian"]
    p2_candidates = [[], [2, 4], [2, 4], [0.01, 0.05, 0.1, 1, 10, 50, 100]]
    p3_candidates = ['Sample-Scale']

    n2 = np.zeros([len(p1_candidates), 1])
    for i2 in range(len(p1_candidates)):
        n2[i2, 0] = max(1, len(p2_candidates[i2]))

    for i1 in range(len(p1_candidates)):
        for i2 in range(1, max(int(n2[i1, 0]), 1)):
            for i3 in range(len(p3_candidates)):
                tmp = p2_candidates[i1]

                if p1_candidates[i1] == 'Gaussian':
                    options.append(
                        {
                            "KernelType": p1_candidates[i1],
                            "normType": p3_candidates[i3],
                            "t": tmp[i2]
                        }
                    )
                elif p1_candidates[i1] == 'Polynomial' or p1_candidates[i1] == 'PolyPlus':
                    options.append(
                        {
                            "KernelType": p1_candidates[i1],
                            "normType": p3_candidates[i3],
                            "d": tmp[i2]
                        }
                    )
    return options


# build GLSPFS params
# local_type_candi = {'LPP', 'LLE', 'LTSA'};
# knn_size_candi = 5;
# lambda1_candi = 10.^[-3:0];
# lambda2_candi = 10.^[-3:0];
def get_GLSPFS_params():
    individuals = []
    kernelOptions = get_GLSPFS_kernel_options()

    local_type_candi = ["LPP", "LLE", "LTSA"]
    knn_size_candi = [5, 8, 10]
    lambda1_candi = [math.pow(10, x) for x in range(-5, 5)]
    lambda2_candi = [math.pow(10, x) for x in range(-5, 5)]

    for i1 in range(len(local_type_candi)):
        for i3 in range(len(knn_size_candi)):
            for i4 in range(len(lambda1_candi)):
                for i5 in range(len(lambda2_candi)):
                    for i6 in range(len(kernelOptions)):
                        individuals.append(
                            {
                                "local_type": local_type_candi[i1],
                                "local_lpp_sigma": [],
                                "local_ltsa_embedded_dim": [],
                                "local_k": knn_size_candi[i3],
                                "lambda1": lambda1_candi[i4],
                                "lambda2": lambda1_candi[i5],
                                "global_kernel_option": kernelOptions[i6]
                            }
                        )
    return np.array(individuals)


#  iDetect parameters  ####
# it = 20;
# distance = {'euclidean','block'};
# sigma = 10.^[-5:0];
# lambda = 10.^[1:3];
# new_lambda = 2.^[1:12];
def get_iDetect_params(default_configs):
    if default_configs:
        return np.array([{
            "distance": "euclidean",
            "it": 30,
            "sigma": 1,
            "lambda": 2
        }])

    individuals = []
    distance = ["euclidean", "block"]
    it = range(10, 50, 10)
    sigma = [math.pow(10, x) for x in range(-8, 8)]
    lamb = [math.pow(10, x) for x in range(1, 20)]

    for i1 in range(len(distance)):
        for i2 in range(len(it)):
            for i3 in range(len(sigma)):
                for i4 in range(len(lamb)):
                    individuals.append(
                        {
                            "distance": distance[i1],
                            "it": it[i2],
                            "sigma": sigma[i3],
                            "lambda": lamb[i4]
                        }
                    )

    return np.array(individuals)


def get_LS_params(default_configs):
    if default_configs:
        return np.array([{
            "mode_metric": ["euclidean"],
            "mode_weight": ["heatKernel"],
            "neighborMode": "knn",
            "k": 5,
            "t": 1
        }])

    individuals = []
    mode_metric = ["euclidean", "cosine"]
    mode_weight = ["binary", "heatKernel", "cosine"]

    k = range(3, 20, 2)
    t = range(1, 10, 2)

    for i1 in range(len(mode_metric)):
        for i2 in range(len(mode_weight)):
            if (mode_metric[i1] == "euclidean" and mode_weight[i2] == "cosine")\
                    or (mode_metric[i1] == "cosine" and mode_weight[i2] == "heatKernel"):
                continue
            for i3 in range(len(k)):
                for i4 in range(len(t)):
                    individuals.append(
                        {
                            "mode_metric": mode_metric[i1],
                            "mode_weight": mode_weight[i2],
                            "neighborMode": "knn",
                            "k": k[i3],
                            "t": t[i4]
                        }
                    )

    return np.array(individuals)


def get_SPEC_params(objs, default_configs):
    if default_configs:
        return np.array([{
                "mode_metric": ["euclidean"],
                "mode_weight": ["heatKernel"],
                "neighborMode": "knn",
                "k": 5,
                "t": 1,
                "style": -1
                }])

    individuals = []
    mode_metric = ["euclidean", "cosine"]
    mode_weight = ["binary", "heatKernel", "cosine"]

    k = range(3, 20, 2)
    t = range(1, 10, 2)
    style = range(-1, objs, 2)

    for i1 in range(len(mode_metric)):
        for i2 in range(len(mode_weight)):
            if (mode_metric[i1] == "euclidean" and mode_weight[i2] == "cosine")\
                    or (mode_metric[i1] == "cosine" and mode_weight[i2] == "heatKernel"):
                continue
            for i3 in range(len(k)):
                for i4 in range(len(t)):
                    for i5 in range(len(style)):
                        individuals.append(
                            {
                                "mode_metric": mode_metric[i1],
                                "mode_weight": mode_weight[i2],
                                "neighborMode": "knn",
                                "k": k[i3],
                                "t": t[i4],
                                "style": style[i5]
                            }
                        )

    return np.array(individuals)
