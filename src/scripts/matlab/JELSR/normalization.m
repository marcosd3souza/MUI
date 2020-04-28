function data_norm = normalization(data)
% This function normalize input data matrix
% Parameters
% ----------
% data: N x D matrix, where each row represents a sample and each column
% represents a feature
% 
% Returns
% -------
% data_norm: N x D matrix, where the mean of each feature is set to be
% zeros and the standard deviation of each feature is set to be ones.

% size of dataset
[n_instances,n_features] = size(data);
data_norm = zeros(n_instances,n_features);

% normalization
for j = 1:n_features
    tmp_mean = mean(data(:,j));
    tmp_std = std(data(:,j));
    data_norm(:,j) = (data(:,j)-tmp_mean)/tmp_std;
end

end