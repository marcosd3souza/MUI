function fs_unsup_spec_single_func(dataset, exp_settings, algo_settings)
%feature selection by SPEC

%======================setup===========================
FeaNumCandi = exp_settings.FeaNumCandi;
%nKmeans = exp_settings.nKmeans;
prefix_mdcs = [];
if isfield(exp_settings, 'prefix_mdcs')
    prefix_mdcs = exp_settings.prefix_mdcs;
end
%======================================================

%disp(['dataset:',dataset]);
%[X, Y] = extractXY(dataset);
[nSmp,nDim] = size(dataset);
nClass = 0;%length(unique(Y));
X = dataset;

%===================setup=======================
styleCandi = [1];
expLamCandi = [0.25, 1, 4];
funcCandi = [1, 2, 3];
s1 = optSigma(X);
kernelParamCell = buildParamKernel({'Gaussian'}, {sqrt(2.^[-4:2]) * s1}, {''});
paramCell = fs_unsup_spec_build_param(kernelParamCell, styleCandi, expLamCandi, funcCandi);
%===============================================

disp('SPEC ...');
t_start = clock;
feaSubsets = cell(length(paramCell), 1);
parfor i1 = 1:length(paramCell)
    fprintf(['SPEC parameter search %d out of %d...\n'], i1, length(paramCell));
    configFileName = strcat(exp_settings.configFolder,"/config_SPEC_", exp_settings.datasetName, "_", num2str(i1),".txt");

    param = paramCell{i1}; 

    save("-text",configFileName, 'param');

    K = constructKernel(X, X, paramCell{i1}.kernelOption);
    wFeat = fs_unsup_spec( K, X, [], paramCell{i1} );

    scoreFileName = strcat(exp_settings.scoreFolder,"/scores_SPEC_", exp_settings.datasetName, "_config_", num2str(i1),".csv");
    dlmwrite(scoreFileName, wFeat');
    %[~, idx] = sort(wFeat,'descend');
    %feaSubsets{i1,1} = idx;
end
t_end = clock;
t1 = etime(t_end,t_start);
disp(['exe time: ',num2str(t1)]);

t_start = clock;
disp('evaluation ...');
%res_aio = cell(length(paramCell), length(FeaNumCandi));
%for i2 = 1:length(FeaNumCandi)
%    for i1 = 1:length(paramCell)
%        fprintf('GLSPFS parameter evaluation %d outof %d  ... %d out of %d...\n', i2, length(FeaNumCandi), i1, length(paramCell));
%        idx = feaSubsets{i1,1};
%        res_aio{i1, i2} = evalUnSupFS(X, Y, idx(1:FeaNumCandi(i2)), struct('nKm', nKmeans));
%    end
%end
%[res_gs, res_gs_ps] = grid_search_fs(res_aio);
%res_gs.feaset = FeaNumCandi;
t_end = clock;
t2 = etime(t_end,t_start);
disp(['exe time: ',num2str(t2)]);
%res_gs.time = t1;
%res_gs.time2 = t2;

%save(fullfile(prefix_mdcs, [dataset, '_best_result_GLSPFS.mat']),'FeaNumCandi','res_gs','res_aio', 'res_gs_ps');
end
