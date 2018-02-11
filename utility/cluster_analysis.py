# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
import pandas as pd
import math
import statistics as stat

def select_n_clusters(dataset):
    cluster_range = range( 1, 20 )
    cluster_errors = []
    
    last_inertia = 0;
    best_k = 0;
    best_diff = 0;
    
    for num_clusters in cluster_range:
      clusters = KMeans(n_clusters=num_clusters, init='k-means++', n_init=20, max_iter=30,
                        tol=0.0001, precompute_distances=True, verbose=0,
                        random_state=None, copy_x=True, n_jobs=-1)
      
      clusters.fit( dataset )
      cluster_errors.append( clusters.inertia_ )
      
      if math.fabs((2 * clusters.inertia_) - last_inertia) > best_diff and last_inertia != 0:
          best_diff = math.fabs((2 * clusters.inertia_) - last_inertia);
          best_k = num_clusters;
      
      last_inertia = clusters.inertia_
    
    print("best k: "+ str(best_k))  
    return cluster_errors, cluster_range
    #return best_k


dataset_file_name = "../train_datasets/ALLAML_dataset.csv"
dataset = pd.read_csv(dataset_file_name, index_col=False, sep=" ");
dataset = dataset.drop(['Y'], axis=1)

cluster_errors, cluster_range = select_n_clusters(dataset)
clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )