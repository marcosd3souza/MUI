function fs_unsup_idetect_single_func(dataset, exp_settings, algo_settings)
%feature selection by iDetect

%===================setup=======================

it = 20;
% 0: euclidean
% 1: block
distance = {'euclidean','block'};
sigma = 10.^[-5:0];
lambda = 10.^[1:3];

%Para.sigma:  kernel width
%Para.lambda:  regularization parameter(critical)

%GDS183
%Para.sigma = 0.1;
%Para.lambda = 75;

paramCell = fs_unsup_idetect_build_param(it, distance, sigma, lambda);
%===============================================

disp('IDetect ...');
t_start = clock;

parfor i1 = 1:length(paramCell)
    fprintf(['IDetect parameter search %d out of %d...\n'], i1, length(paramCell));
    %configFileName = strcat(exp_settings.configFolder,"/config_iDetect_", exp_settings.datasetName, "_", num2str(i1),".txt");

    param = paramCell{i1}; 

    %save("-text",configFileName, 'param');

    [Objective, Weight, History] = iDetect(dataset', param);

    scoreFileName = strcat(exp_settings.scoreFolder,"/scores_iDetect_", exp_settings.datasetName, "_config_", num2str(i1),".csv");
    disp('saving in:')
    disp(scoreFileName)
    dlmwrite(scoreFileName, Weight);
    %[~, idx] = sort(wFeat,'descend');
    %feaSubsets{i1,1} = idx;
end

t_end = clock;
t1 = etime(t_end,t_start);
disp(['exe time: ',num2str(t1)]);

end
