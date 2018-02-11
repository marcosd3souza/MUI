import numpy as np
import sklearn.utils.linear_assignment_ as la
from sklearn.metrics import accuracy_score
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import f1_score
from sklearn.cluster import KMeans
#from rpy2.robjects.packages import importr
#import rpy2.robjects as robjects
#from rpy2.robjects import pandas2ri

#import rpy2.robjects.numpy2ri
#rpy2.robjects.numpy2ri.activate()

#pip install rpy2
#r = robjects.r
#fpc = importr('fpc')
#stats = importr('stats')

def best_map(l1, l2):
    """
    Permute labels of l2 to match l1 as much as possible
    """
    if len(l1) != len(l2):
        print("L1.shape must == L2.shape")
        exit(0)

    label1 = np.unique(l1)
    n_class1 = len(label1)

    label2 = np.unique(l2)
    n_class2 = len(label2)

    n_class = max(n_class1, n_class2)
    G = np.zeros((n_class, n_class))

    for i in range(0, n_class1):
        for j in range(0, n_class2):
            ss = l1 == label1[i]
            tt = l2 == label2[j]
            G[i, j] = np.count_nonzero(ss & tt)

    A = la.linear_assignment(-G)

    new_l2 = np.zeros(l2.shape)
    for i in range(0, n_class2):
        new_l2[l2 == label2[A[i][1]]] = label1[A[i][0]]
    return new_l2.astype(int)


def evaluation(X_selected, n_clusters, y):
    """
    This function calculates ARI, ACC and NMI of clustering results

    Input
    -----
    X_selected: {numpy array}, shape (n_samples, n_selected_features}
            input data on the selected features
    n_clusters: {int}
            number of clusters
    y: {numpy array}, shape (n_samples,)
            true labels

    Output
    ------
    nmi: {float}
        Normalized Mutual Information
    acc: {float}
        Accuracy
    """
    k_means = KMeans(n_clusters=n_clusters, init='k-means++', n_init=20, max_iter=30,
                     tol=0.0001, precompute_distances=True, verbose=0,
                     random_state=None, copy_x=True, n_jobs=1)

    k_means.fit(X_selected)
    y_predict = k_means.labels_
    
    #inercia = k_means.inertia_
    inertia = k_means.inertia_

    # calculate NMI
    nmi = normalized_mutual_info_score(y, y_predict)
    #nmi = 0
    
    #calculate corrected rand
    corrected_rand = adjusted_rand_score(y, y_predict)
    corrected_rand = 0
    
    #calculate f-measure
    #f_measure = f1_score(y, y_predict, average='macro');  
    f_measure = 0

    # calculate ACC
    
    y_permuted_predict = best_map(y, y_predict)
    acc = accuracy_score(y, y_permuted_predict)
    
   # dgene = stats.dist(X_selected, method='euclidean')
    
    #fpc_result = fpc.cluster_stats(dgene, k_means.labels_, G2 = True, G3 = True, silhouette=False)
    #stats_fpc = pandas2ri.ri2py(fpc_result)
    
    #dunn = stats_fpc[24][0]
    #dunn2 = stats_fpc[25][0]
    #entropy = stats_fpc[26][0]
    #ch = stats_fpc[28][0]

    #return dunn, dunn2, entropy, ch, inertia, nmi, acc, corrected_rand, f_measure
    return inertia, nmi, acc, corrected_rand, f_measure
