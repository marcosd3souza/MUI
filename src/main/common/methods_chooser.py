# -*- coding: utf-8 -*-
import math
from functools import partial

from algorithms.python.unsupervised import SPEC
from algorithms.python.unsupervised import lap_score
from algorithms.python.unsupervised import MCFS
from algorithms.python.unsupervised import NDFS
from algorithms.python.unsupervised import UDFS
from algorithms.python.genetic import parameters_selection as genetic
from helpers import logger
from helpers.construct_W import construct_W
import common.parameters as params

from datetime import datetime

# pip install oct2py
from oct2py import octave
import numpy as np
import common.commons as commons


def run_method(data, method, default_method_configs):
    octave.restart()

    if method == "SPEC":
        return run_SPEC(data, default_method_configs)
    elif method == "MCFS":
        return run_MCFS(data)
    elif method == "LS":
        return run_lap_score(data, default_method_configs)
    elif method == "NDFS":
        return run_NDFS(data)
    elif method == "UDFS":
        return run_UDFS(data)
    elif method == "iDetect":
        # octave.addpath("algorithms/matlab")
        return run_iDetect(data, default_method_configs)
    elif method == "GLSPFS":
        # octave.addpath("algorithms/matlab/GLSPFS")
        return run_GLSPFS(data, default_method_configs)
    elif method == "FSASL":
        octave.addpath("algorithms/matlab/FSASL")
        return run_FSASL(data)
    elif method == "JELSR":
        octave.addpath("algorithms/matlab/JELSR")
        return run_JELSR(data)


def run_SPEC(X, default_configs):
    logger.log("running SPEC ...")
    dataset = np.copy(X)
    objs = dataset.shape[0]
    features = dataset.shape[1]

    # select scores rankings by
    # best parameters using genetic algorithms
    param_population = params.get_SPEC_params(objs, default_configs)
    func_construct_w = partial(construct_W, X=dataset)
    func_fit = partial(SPEC.spec, X=dataset)
    scores = genetic.select_best_rankings(features, param_population, 'SPEC', None,
                                          lambda param: func_fit(**param),
                                          lambda arg: func_construct_w(**arg), default_configs)

    if not default_configs:
        scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_MCFS(dataset):
    kwargs = {"metric": "euclidean", "neighborMode": "knn", "weightMode": "heatKernel", "k": 5, 't': 1}
    W = construct_W(dataset, **kwargs)
    Weight = MCFS.mcfs(dataset, n_selected_features=dataset.shape[1], W=W)
    return Weight.max(1)


def run_UDFS(dataset):
    Weight = UDFS.udfs(dataset, gamma=0.1, n_clusters=5, verbose=True)
    return Weight.max(1)


def run_lap_score(X, default_configs):
    logger.log("running LS ...")
    dataset = np.copy(X)
    features = dataset.shape[1]

    # select scores rankings by
    # best parameters using genetic algorithms
    param_population = params.get_LS_params(default_configs)
    func_construct_w = partial(construct_W, X=dataset)
    func_fit = partial(lap_score.lap_score, X=dataset)
    scores = genetic.select_best_rankings(features, param_population, 'LS', None,
                                          lambda param: func_fit(**param),
                                          lambda arg: func_construct_w(**arg), default_configs)

    if not default_configs:
        scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_NDFS(dataset):
    logger.log("running NDFS ...")
    kwargs = params.get_W_params()
    cols = dataset.shape[1]

    scores = np.empty([cols, 1])
    scores[:, 0] = None

    index = 1
    total_configs = 24

    # abs(round(pearsonr(a, b)[0], 3)) >= 0.985

    for mode in kwargs['mode']:
        for k in kwargs['k']:
            arg = {"k": k, "t": 1,
                   "metric": mode['metric'],
                   "weightMode": mode['weightMode'],
                   "neighborMode": "knn"}

            dt_1 = datetime.now()
            W = construct_W(dataset, **arg)

            Weight = NDFS.ndfs(dataset, W=W, n_clusters=5, verbose=True)
            dt_2 = datetime.now()

            # calculate euclidean norm to all clusters
            # np.sqrt(np.sum(np.square(np.array([[2,4,4], [3,5,3], [1, 3, 5]])), axis=1))
            weights = np.sqrt(np.sum(np.square(Weight), axis=1))
            scores = np.append(scores, weights[:, None], 1)

            logger.log("NDFS - sum of scores: " + str(sum(scores[:, index])), False)
            time = dt_2 - dt_1
            logger.log("run NDFS config " + str(index) + " of " + str(total_configs) + " in: " + str(time), False)
            index = index + 1

    scores_NDFS = commons.remove_duplicated_rankings(scores)
    return scores_NDFS


# @jit
def run_iDetect(X, default_configs):
    logger.log("running iDetect ...")
    param_population = params.get_iDetect_params(default_configs)
    data = np.copy(X)
    n_features = data.shape[0]

    scores = genetic.select_best_rankings(n_features, param_population, 'iDetect', data, None, None, default_configs)

    if not default_configs:
        scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_FSASL(data):
    n_features = data.shape[1]
    # arg = {"nKmeans": 5, "FeaNumCandi": n_features}

    # FSASL parameters ###
    # alphaCandi = 10.^[-5:5];
    # betaCandi = 10.^[-5:5];
    # gammaCandi = [0.001, 0.005, 0.01, 0.05, 0.1];
    # maxIter = 3;
    # nnCandi = 1;
    paramCell = octave.get_FSASL_params(data)

    scores = np.empty([n_features, 1])
    scores[:, 0] = None

    total_configs = len(paramCell)
    index = 1
    nClass = 5

    for i in range(1, total_configs):
        dt_1 = datetime.now()
        # FSASL(X', nClass, paramCell{i1})
        new_col = octave.FSASL(data.T, nClass, paramCell[i])

        # apply euclidean norm
        new_col = np.sqrt(np.sum(np.square(new_col), axis=1))

        dt_2 = datetime.now()
        time = dt_2 - dt_1
        logger.log("FSASL run config " + str(index) + " of " + str(total_configs) + " in: " + str(time) + " ms", True)
        index = index + 1

        if sum(new_col[:, ]) > 0:
            scores = np.append(scores, new_col[:, None], 1)
            logger.log("FSASL - sum of scores: " + str(sum(scores[:, i])), False)

    scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_JELSR(x):
    data = np.copy(x)
    n_features = data.shape[1]
    # JELSR parameters ###
    # r1Candi = 10. ^ [-5:5];
    # r2Candi = 10. ^ [-5:5];
    # knnCandi = 5;
    # weightCandi = {'lle', 'lpp'};
    paramCell = octave.get_JELSR_params(data)

    scores = np.empty([n_features, 1])
    scores[:, 0] = None

    total_configs = len(paramCell)
    index = 1

    for i in range(1, total_configs):
        dt_1 = datetime.now()
        W = octave.computeLocalStructure(data, paramCell[i]['weightMode'], paramCell[i]['k'], paramCell[i]['t'])
        new_col = octave.fs_unsup_jelsr(data, W, [], paramCell[i]['alpha'], paramCell[i]['beta'])

        # apply euclidean norm
        # new_col = np.sqrt(np.sum(np.square(new_col), axis=1))

        dt_2 = datetime.now()
        time = dt_2 - dt_1
        logger.log("JELSR run config " + str(index) + " of " + str(total_configs) + " in: " + str(time) + " ms", True)
        index = index + 1

        if sum(new_col[:, ]) > 0:
            scores = np.append(scores, new_col, 1)
            logger.log("JELSR - sum of scores: " + str(sum(scores[:, i])), False)

    scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_GLSPFS(X, state_of_art):
    logger.log("running GLSPFS ...")
    param_population = params.get_GLSPFS_params()
    data = np.copy(X)
    n_features = data.shape[1]

    scores = genetic.select_best_rankings(n_features, param_population, 'GLSPFS', data, None, None, state_of_art)

    if not state_of_art:
        scores = commons.remove_duplicated_rankings(scores)
    return scores


def run_old_GLSPFS(X):
    data = np.copy(X)
    n_features = data.shape[1]
    index = 1
    scores = np.empty([n_features, 1])
    scores[:, 0] = None

    # FIXME use selected K
    for nKmeans in [10]:
        arg = {"nKmeans": nKmeans, "FeaNumCandi": n_features}
        params = octave.get_GLSPFS_params(data, arg)

        total_configs = len(params)

        for i in range(1, total_configs):
            dt_1 = datetime.now()

            K = octave.constructKernel(data, data, params[i]['global_kernel_option'])
            L = octave.computeLocalStructure(data, params[i]['local_type'], params[i]['local_k'],
                                             params[i]['local_lpp_sigma'], params[i]['local_ltsa_embedded_dim'])
            new_col = octave.fs_unsup_glspfs(data, K, L, params[i]['lambda1'], params[i]['lambda2'], n_features)

            dt_2 = datetime.now()
            time = dt_2 - dt_1
            logger.log("run config " + str(index) + " of " + str(total_configs) + " in: " + str(time) + " ms", True)
            index = index + 1

            if sum(new_col[:, ]) > 0:
                scores = np.append(scores, new_col, 1)
                logger.log("GLSPFS - sum of scores: " + str(sum(scores[:, i])), False)

    scores = commons.remove_duplicated_rankings(scores)
    return scores
