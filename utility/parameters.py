# -*- coding: utf-8 -*-

#####  iDetect parameters  ####
# it = 20;
# distance = {'euclidean','block'};
# sigma = 10.^[-5:0];
# lambda = 10.^[1:3];
# new_lambda = 2.^[1:12];
import math

def get_iDetect_params():
    
    kwargs = {"it": [15],"distance": ["euclidean", "block"],
          "sigma": [math.pow(10, x) for x in range(-5, 0, 2)],
          "lambda": [math.pow(2, x) for x in range(1, 11, 2)]}
    
    return kwargs

def get_W_params():
    
    #kwargs = {"metric": "euclidean", 
    #"neighborMode": "knn", "weightMode": "heatKernel", 
    #"k": 5, 't': 1}
    kwargs = {"mode":[{"metric": "euclidean", "weightMode": "heatKernel"},
                      {"metric": "cosine", "weightMode": "cosine"},
                      {"metric": "euclidean","weightMode": "binary"},
                      {"metric": "cosine","weightMode": "binary"}],
          "neighborMode": ["knn"],
          "k": [5,8], 't': 1}
    
    return kwargs