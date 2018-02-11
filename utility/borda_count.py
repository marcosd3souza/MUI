#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 09:19:10 2018

@author: marcosdesouza
"""

from datetime import datetime

def borda_sort(ranks):
    scores = {}
    for l in ranks:
        for idx, elem in enumerate(reversed(l)):
            if not elem in scores:
                scores[elem] = 0
            scores[elem] += idx
    return sorted(scores.keys(), key=lambda elem: scores[elem], reverse=True)

rank_a = eval(str([1, 3, 4, 2]))
rank_b = eval(str([3, 2 , 1, 4]))

ranks = [rank_a, rank_b];
#ranks = [ random.sample(range(50000), 50000) for x in range(100) ] 


dt_1 = datetime.now()
result = borda_sort(ranks);
dt_2 = datetime.now()

total_time = dt_2 - dt_1
print("total time elapsed: "+ str(total_time))

#print (str(result))