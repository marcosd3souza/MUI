function [paramCell] = get_GLSPFS_params(dataset)
%feature selection by FSASL

X = dataset;

%===================setup=======================
alphaCandi = 10.^[-3:2];
betaCandi = 10.^[-3:2];
gammaCandi = [0.001, 0.05, 0.1];
maxIter = 3;
nnCandi = 5;
paramCell = fs_unsup_fsasl_build_param({'LARS'}, {gammaCandi}, nnCandi, ...
    alphaCandi, betaCandi, {'LS21'}, maxIter);
%===============================================
end
