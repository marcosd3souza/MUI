# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 00:45:26 2017

@author: marcos
"""
import numpy as np
import Chooser as cs
import scores_cutoff as cuttof
from utility import unsupervised_evaluation, normalize, borda_count, evaluate_merged_ranking
import pandas as pd
import scipy.io
import scipy as sp
from functools import partial
from itertools import repeat
from datetime import datetime
from execution import select_best_ranking as FSelection
from sklearn.feature_selection import VarianceThreshold

def run_parallel_FS():
    datasets = ["warpPIE10P", "pixraw10P", "warpAR10P", "TOX171", "ALLAML", "Carcinom", "SMK_CAN", "ProstateGE"]
    #text datasets = ["BASEHOCK", "RELATHE", "PCMAC"]
    methods = ["LS", "SPEC", "iDetect", "GLSPFS"]
    cols=["dataset", "total_features", "method_FS", "Method_cut", "selected_features", "inercia", "inercia/n_features", "nmi","accuracia", "corrected_rand", "f_measure"];
    dataset_folder_file_name = "train_datasets/filtered/"
    row = []
    result = pd.DataFrame(columns=cols)
    
    for dataset_name in datasets:

        dataset_file_name = dataset_folder_file_name +"filtered_"+ dataset_name + ".csv"
        dataset = pd.read_csv(dataset_file_name, index_col=False, sep=" ");

        #print("rankings: "+str(rankings.shape))
        
        y = list(dataset.loc[:, 'Y']);
        dataset = dataset.drop(['Y'], axis=1)
        
        data_transposed = dataset.T
        dataset = normalize.get_normalized_data(data_transposed).T
        
        #print("dataset before: "+ str(dataset.shape));
        
        # eliminate features < 20% variance
        #sel = VarianceThreshold(threshold=(.1 * (1 - .1)))
        #data = sel.fit_transform(dataset.values)
        
        #if (data.shape[1] >= 10):
        #    dataset = pd.DataFrame(data);
            
        n_features = dataset.shape[1];
        
        rankings = np.empty([n_features, 1])
        
        for method in methods:
            
            row, best_rank = FSelection.perform_FS_parallel(dataset, dataset_name, method, y)
            current_row = pd.DataFrame(row, columns=cols)
            result = pd.concat([result, current_row])
            
            rank = pd.Series(best_rank);
            print("best rank: "+str(rank.shape))
            
            rankings = np.append(rankings, rank[:, None] , 1)
       
        np.savetxt("result_ranks_"+dataset_name+".csv", rankings, delimiter=" ");
        
        # LS - SPEC
        merged_ranks_LS_SPEC = borda_count.borda_sort([rankings[:,1], rankings[:,2]])
        borda_result_LS_SPEC = evaluate_borda(merged_ranks_LS_SPEC, dataset, dataset_name, 'Borda_LS_SPEC', y);
        result = pd.concat([result, borda_result_LS_SPEC])
        
        # LS - iDetect
        merged_ranks_LS_Idetect = borda_count.borda_sort([rankings[:,1], rankings[:,3]])
        borda_result_LS_Idetect = evaluate_borda(merged_ranks_LS_Idetect, dataset, dataset_name, 'Borda_LS_IDetect', y);
        result = pd.concat([result, borda_result_LS_Idetect])
        
        # LS - GLSPFS
        merged_ranks_LS_GLSPFS = borda_count.borda_sort([rankings[:,1], rankings[:,4]])
        borda_result_LS_GLSPFS = evaluate_borda(merged_ranks_LS_GLSPFS, dataset, dataset_name, 'Borda_LS_GLSPFS', y);
        result = pd.concat([result, borda_result_LS_GLSPFS])
        
        #SPEC - iDetect
        merged_ranks_SPEC_IDetect = borda_count.borda_sort([rankings[:,2], rankings[:,3]])
        borda_result_SPEC_IDetect = evaluate_borda(merged_ranks_SPEC_IDetect, dataset, dataset_name, 'Borda_SPEC_iDetect', y);
        result = pd.concat([result, borda_result_SPEC_IDetect])
        
        #SPEC - GLSPFS
        merged_ranks_SPEC_GLSPFS = borda_count.borda_sort([rankings[:,2], rankings[:,4]])
        borda_result_SPEC_GLSPFS = evaluate_borda(merged_ranks_SPEC_GLSPFS, dataset, dataset_name, 'Borda_SPEC_GLSPFS', y);
        result = pd.concat([result, borda_result_SPEC_GLSPFS])
        
        #iDetect - GLSPFS
        merged_ranks_iDetect_GLSPFS = borda_count.borda_sort([rankings[:,3], rankings[:,4]])
        borda_result_iDetect_GLSPFS = evaluate_borda(merged_ranks_iDetect_GLSPFS, dataset, dataset_name, 'Borda_iDetect_GLSPFS', y);
        result = pd.concat([result, borda_result_iDetect_GLSPFS])
        
        #All
        merged_ranks_all = borda_count.borda_sort([rankings[:,1], rankings[:,2], rankings[:,3], rankings[:,4]])
        borda_result_all = evaluate_borda(merged_ranks_all, dataset, dataset_name, 'Borda_ALL', y);
        result = pd.concat([result, borda_result_all])
        
        result.to_csv("result_all_fea_"+dataset_name+".csv", sep=" ")
    

def evaluate_borda(merged_ranks, dataset, dataset_name, label, y):

    n_cluster = max(y);
    
    result_borda = evaluate_merged_ranking.evaluate(merged_ranks, dataset, n_cluster, y, dataset_name, label)
    
    cols=["dataset", "total_features", "method_FS", "Method_cut", "selected_features", "inercia", "inercia/n_features", "nmi","accuracia", "corrected_rand", "f_measure"];
    
    result_tb = pd.DataFrame(result_borda, columns=cols);
    
    return result_tb


dt_1 = datetime.now()

run_parallel_FS()

dt_2 = datetime.now()
total_time = dt_2 - dt_1
print("total time elapsed: "+ str(total_time))

#result = pd.concat([result_from_LS])


"""
if __name__ == '__main__':
    main()
"""
