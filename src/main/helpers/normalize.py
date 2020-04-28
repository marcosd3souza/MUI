# -*- coding: utf-8 -*-
# idetect normalization

# Normalize to [0, 1]
#[MIN,~] = min(patterns,[],2);
#[MAX,~] = max(patterns,[],2);
#for n=1:dim
#    if(MIN(n)==MAX(n))
#        patterns(n,:) = 0;
#    else
#        patterns(n,:) = (patterns(n,:)-MIN(n))/(MAX(n)-MIN(n));
#    end
#end

def get_normalized_data(data):
    n_features = data.shape[0]
    
    MINS = data.min(axis=1).iloc[0:n_features];
    MAXS = data.max(axis=1).iloc[0:n_features];

    for n in range(0, n_features):
        if MINS[n] == MAXS[n]:
            data.iloc[n, :] = 0
        else :
            data.iloc[n, :] = (data.iloc[n, :] - MINS[n]) / (MAXS[n] - MINS[n])
            
    return data