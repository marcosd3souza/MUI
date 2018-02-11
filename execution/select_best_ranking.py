# -*- coding: utf-8 -*-
import numpy as np
import Chooser as cs
import scores_cutoff as cuttof
from utility import unsupervised_evaluation, normalize
import pandas as pd
import scipy.io
import scipy as sp
from functools import partial
from itertools import repeat
import math
import utility.parameters as params
from sklearn.feature_selection import VarianceThreshold

def perform_FS_parallel(dataset, dataset_name, method, y):
    
    result = [];
    
    #cutoff_methods = ['all_features']
    cutoff_methods = ['second_derivate', 'percent', 'all_features']
    
    n_features = dataset.shape[1];
    n_clusters = max(y);
    
    print("dataset after: "+ str(dataset.shape));
    
    for magic_number in range(10,int(0.2*n_features),50):
        cutoff_methods.append(magic_number)
    
    if method == 'iDetect':
        numpy_data = dataset.values
        all_configs_by_FS = cs.run_method(numpy_data.T, method);
    else:
        numpy_data = dataset.values
        all_configs_by_FS = cs.run_method(numpy_data, method);
        
    best_nmi = 0;
    best_corrected_rand = 0;
    best_acc = 0;
    best_f_measure = 0;
    best_cutoff_method = "";
    best_cutoff_point = 0;
    #last_inertia = 0;
    minimum_inertia = 0;
    best_inertia = 0;
    total_configs = all_configs_by_FS.shape[1];
    index = 1;
    
    for column in range(0, total_configs):
        
        print("evaluate "+method+" config "+str(index)+" of "+str(total_configs))
        index = index + 1
        
        scores_by_FS = all_configs_by_FS[:, column]
        scores_df = pd.DataFrame({"feature": range(0,n_features), "score":scores_by_FS});
        scores_sorted = scores_df.sort_values(by="score", ascending = False);
        
        values = pd.DataFrame(scores_sorted.iloc[:,1]);
        values.reset_index(drop=True, inplace=True)          
        
        
        for cutoff_method in cutoff_methods:
            if cutoff_method == 'second_derivate':
                cuttof_point = cuttof.get_cut_off_point_by_second_derivate(values);
                
                if cuttof_point > int(0.6 * n_features):
                    cuttof_point = 0
                    
            elif cutoff_method == 'percent':
                cuttof_point = cuttof.get_cut_off_point_by_percent(values);                    
            elif cutoff_method == 'all_features':
                cuttof_point = n_features;
            else:
                cuttof_point = cutoff_method
        
           # print(method+ " - trying cuttof method: "+str(cutoff_method))
            if cuttof_point >= 10:
                features_selected = scores_sorted.iloc[0:cuttof_point,0];
                dataset_filtered = dataset.iloc[:,features_selected];
                
                inertia, nmi, acc, corrected_rand, f_measure = unsupervised_evaluation.evaluation(X_selected=dataset_filtered.values, n_clusters=n_clusters, y=y);
                
                #print("inertia : "+ str(inertia));
                #print("nmi : "+ str(nmi));

                if (inertia/cuttof_point < minimum_inertia or minimum_inertia == 0):
                    
                    features_rank = pd.DataFrame(scores_sorted.loc[:,'feature']);
                    best_ranking = features_rank['feature'].tolist();
                    #print("first features: "+str(best_ranking[1]));
        
                    minimum_inertia = inertia/cuttof_point;
                    
                    best_inertia = inertia
                    best_nmi = nmi
                    best_corrected_rand = corrected_rand
                    best_cutoff_method = cutoff_method
                    best_cutoff_point = cuttof_point
                    best_f_measure = f_measure
                    best_acc = acc
                #break
                #last_inertia = inertia;
        #break
    result.append([dataset_name, n_features, method, best_cutoff_method, best_cutoff_point, best_inertia, minimum_inertia, best_nmi, best_acc, best_corrected_rand, best_f_measure]);
    
    return result, best_ranking;
