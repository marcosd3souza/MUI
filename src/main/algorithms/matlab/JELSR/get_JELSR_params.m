function [paramCell] = get_JELSR_params(X)
%Unsupervised feature selection using JELSR

%===================setup=======================
r1Candi = 10.^[-2:0];
r2Candi = 10.^[-2:0];
knnCandi = 5;
weightCandi = {'lle', 'lpp'};
s1 = optSigma(X);
disp(s1);
weight_param_Candi = {s1};
paramCell = fs_unsup_jelsr_build_param(knnCandi, weightCandi, weight_param_Candi, r1Candi, r2Candi);
%===============================================