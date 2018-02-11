# -*- coding: utf-8 -*-
from algorithms.python.unsupervised import SPEC
from algorithms.python.unsupervised import lap_score
from algorithms.python.unsupervised import MCFS
from algorithms.python.unsupervised import NDFS
from algorithms.python.unsupervised import UDFS
from utility.construct_W import construct_W

import utility.parameters as params

from datetime import datetime

# pip install oct2py
from oct2py import octave
import numpy as np

def run_method(dataset, method):
    
    octave.restart();
    
    if method == "SPEC":
       return run_SPEC(dataset)
    elif method == "MCFS":
        return run_MCFS(dataset)
    elif method == "LS":
        return run_lap_score(dataset)
    elif method == "NDFS":
        return run_NDFS(dataset)
    elif method == "UDFS":
        return run_UDFS(dataset)
    elif method == "iDetect":
        octave.addpath("algorithms/matlab")
        return run_iDetect(dataset)
    elif method == "GLSPFS":
        octave.addpath("algorithms/matlab/GLSPFS")
        return run_GLSPFS(dataset)
    
def run_SPEC(dataset):
    print("running SPEC ...")
    kwargs = params.get_W_params()
    cols = dataset.shape[1]
    scores_SPEC = np.empty([cols, 1])
    index = 1
    total_configs = 25
    
    for mode in kwargs['mode']:
        for k in kwargs['k']:
            for style in [0, -1, 2]:
                
                arg = {"k":k, "t":1,
                       "metric": mode['metric'],
                       "weightMode": mode['weightMode'],
                       "neighborMode":"knn"}
                
                
                dt_1 = datetime.now()
                W = construct_W(dataset, **arg);
                spec_args = {'style': style};
                spec_args = {'W': W}
                new_row = SPEC.spec(dataset, **spec_args);
                dt_2 = datetime.now()
                
                scores_SPEC = np.append(scores_SPEC, new_row[:, None] , 1)
                print("SPEC - sum of scores: "+ str(sum(scores_SPEC[:, index])))
                time = dt_2 - dt_1
                print("run SPEC config "+str(index)+" of "+str(total_configs)+" in: "+str(time))
                index = index + 1
                #break
            #break
        #break
    
    return scores_SPEC

def run_MCFS(dataset):
    kwargs = {"metric": "euclidean", "neighborMode": "knn", "weightMode": "heatKernel", "k": 5, 't': 1}
    W = construct_W(dataset, **kwargs);
    Weight = MCFS.mcfs(dataset, n_selected_features=dataset.shape[1], W=W);
    return Weight.max(1);

def run_NDFS(dataset):
    kwargs = {"metric": "euclidean", "neighborMode": "knn", "weightMode": "heatKernel", "k": 5, 't': 1}
    cols = dataset.shape[1]
    scores_NDFS = np.empty([cols, 1])
    
    W = construct_W(dataset, **kwargs);
    Weight = NDFS.ndfs(dataset, W=W, n_clusters=5, verbose=True);
    
    scores_NDFS = np.append(scores_NDFS, Weight.max(1)[:, None], 1);    
    
    return scores_NDFS;

def run_UDFS(dataset):
    Weight = UDFS.udfs(dataset, gamma=0.1, n_clusters=5, verbose=True)
    return Weight.max(1);
    
def run_lap_score(dataset):
    print("running LS ...")
    kwargs = params.get_W_params()
    cols = dataset.shape[1]
    scores_LS = np.empty([cols, 1])
    index = 1
    total_configs = 24
    
    for mode in kwargs['mode']:
        for k in kwargs['k']:
            arg = {"k":k, "t":1,
                   "metric": mode['metric'],
                   "weightMode": mode['weightMode'],
                   "neighborMode":"knn"}
            
            
            dt_1 = datetime.now()
            W = construct_W(dataset, **arg);
            LS_args = {'W': W}
            new_row = lap_score.lap_score(dataset, **LS_args);
            dt_2 = datetime.now()
            
            scores_LS = np.append(scores_LS, new_row[:, None] , 1)
            print("LS - sum of scores: "+ str(sum(scores_LS[:, index])))
            time = dt_2 - dt_1
            print("run LS config "+str(index)+" of "+str(total_configs)+" in: "+str(time))
            index = index + 1
            #break
        #break
    
    return scores_LS

def run_iDetect(data):
    print("running iDetect ...")
    kwargs = params.get_iDetect_params()
    n_features = data.shape[0]
    scores = np.empty([n_features, 1])
    index = 1
    total_configs = len(kwargs['distance']) * len(kwargs['lambda']) * len(kwargs['sigma'])
    it = kwargs['it']
    
    for distance in kwargs['distance']:
        for lam in kwargs['lambda']:
            for sigma in kwargs['sigma']:
                
                dt_1 = datetime.now()
                
                arg = {"it": it,"distance": distance, "sigma": sigma, "lambda": lam}
                new_col = octave.iDetect(data, arg)
                dt_2 = datetime.now()
                scores = np.append(scores, new_col , 1)
                
                time = dt_2 - dt_1
                print("run config "+str(index)+" of "+str(total_configs) + " in: "+str(time)+" ms")
                index = index + 1
    
    return scores

def run_GLSPFS(data):
    
    n_features = data.shape[1]
    scores = np.empty([n_features, 1])
    arg = {"nKmeans":5, "FeaNumCandi":n_features}
    params = octave.get_GLSPFS_params(data, arg)
    
    total_configs = len(params)
    index = 1
    
    for i in range(1, total_configs):
        dt_1 = datetime.now()
        
        K = octave.constructKernel(data, data, params[i]['global_kernel_option'])
        L = octave.computeLocalStructure(data, params[i]['local_type'], params[i]['local_k'], params[i]['local_lpp_sigma'], params[i]['local_ltsa_embedded_dim']);
        new_col = octave.fs_unsup_glspfs(data, K, L, params[i]['lambda1'], params[i]['lambda2'], n_features);
        
        dt_2 = datetime.now()
        time = dt_2 - dt_1
        print("run config "+str(index)+" of "+str(total_configs) + " in: "+str(time)+" ms")
        index = index + 1
        
        if sum(new_col[:,]) > 0:
            scores = np.append(scores, new_col , 1)
            print("GLSPFS - sum of scores: "+ str(sum(scores[:, i])))
    return scores