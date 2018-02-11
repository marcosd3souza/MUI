# -*- coding: utf-8 -*-

from utility import unsupervised_evaluation
import math

def evaluate(features, dataset, n_clusters, y, dataset_name, label):
    cutoff_methods = ['all_features']
    
    n_features = dataset.shape[1]
    
    result = [];
    
    best_nmi = 0
    best_corrected_rand = 0
    best_acc = 0
    best_f_measure = 0
    best_cutoff_method = ""
    best_cutoff_point = 0
    best_inertia = 0
    minimum_inertia = 0;
    #last_inertia = 0;
    
    for magic_number in range(10,int(0.2*n_features),50):
        cutoff_methods.append(magic_number)
    
    for cutoff_method in cutoff_methods:
        if cutoff_method == 'all_features':
            cuttof_point = n_features;
        else:
            cuttof_point = cutoff_method
    
        print("Borda - trying cuttof method: "+str(cutoff_method))
        if cuttof_point > 0:
            
            features_selected = features[0:cuttof_point]
            dataset_filtered = dataset.iloc[:,features_selected];
            
            inertia, nmi, acc, corrected_rand, f_measure = unsupervised_evaluation.evaluation(X_selected=dataset_filtered.values, n_clusters=n_clusters, y=y)
            
            if (inertia/cuttof_point < minimum_inertia or minimum_inertia == 0):
                
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
    result.append([dataset_name, n_features, label, best_cutoff_method, best_cutoff_point, best_inertia, minimum_inertia,  best_nmi, best_acc, best_corrected_rand, best_f_measure]);

    return result;
