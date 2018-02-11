function [paramCell] = get_GLSPFS_params(dataset, exp_settings)
%Unsupervised feature selection using GLSPFS

%======================setup===========================
disp("entrou GLSPFS")
FeaNumCandi = exp_settings.FeaNumCandi;
nKmeans = exp_settings.nKmeans;
prefix_mdcs = [];
if isfield(exp_settings, 'prefix_mdcs')
    prefix_mdcs = exp_settings.prefix_mdcs;
end
%======================================================

%disp(['dataset:',dataset]);
%[X, Y] = extractXY(dataset);
[nSmp,nDim] = size(dataset);
nClass = 0;%length(unique(Y));

%===================setup=======================
local_type_candi = {'LPP', 'LLE', 'LTSA'};
local_type_param_candi = {[], [], []};
knn_size_candi = 5;
lambda1_candi = 10.^[-4:0];
lambda2_candi = 10.^[-4:0];
s1 = optSigma(dataset);
global_kernel_cell_candi = buildParamKernel({'Gaussian'}, {sqrt(2.^[-1]) * s1}, {''});
local_type_param_candi{1} = [sqrt(2.^[-1]) * s1];
local_type_param_candi{3} = [nClass];
paramCell = fs_unsup_glspfs_build_param(local_type_candi, local_type_param_candi, knn_size_candi, ...
    lambda1_candi, lambda2_candi, global_kernel_cell_candi);
%===============================================
end
