function fs_unsup_jelsr_single_func(X, exp_settings)
%Unsupervised feature selection using JELSR

%===================setup=======================
r1Candi = 10.^[-5:5];
r2Candi = 10.^[-5:5];
knnCandi = 5;
weightCandi = {'lle', 'lpp'};
s1 = optSigma(X);
disp(s1);
weight_param_Candi = {s1};
paramCell = fs_unsup_jelsr_build_param(knnCandi, weightCandi, weight_param_Candi, r1Candi, r2Candi);
%===============================================

t_start = clock;
disp('JELSR ...');

parfor i1 = 1:length(paramCell)
    fprintf('JELSR parameter search %d out of %d...\n', i1, length(paramCell));
    configFileName = strcat(exp_settings.configFolder,"/config_JELSR_", exp_settings.datasetName, "_", num2str(i1),".txt");

    param = paramCell{i1}; 

    save("-text",configFileName, 'param');
    
    [~, W] = computeLocalStructure(X, param.weightMode, param.k, param.t);
    W_compute = fs_unsup_jelsr(X, W, [], param.alpha, param.beta);

    scores = sum(W_compute.^2,2);

    scoreFileName = strcat(exp_settings.scoreFolder,"/scores_JELSR_", exp_settings.datasetName, "_config_", num2str(i1),".csv");
    dlmwrite(scoreFileName, scores);

end
t_end = clock;
t1 = etime(t_end,t_start);
disp(['exe time: ',num2str(t1)]);
end
