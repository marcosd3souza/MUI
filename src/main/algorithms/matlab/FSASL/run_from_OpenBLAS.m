data = textread('/home/marcos/Documentos/UFPE/microarray/Experimento/Feature Selection/Algoritmos/GDS183.csv','','delimiter',',','whitespace','"');
exp_settings.FeaNumCandi = size(data, 2);
exp_settings.nKmeans = 5;
[W] = fs_unsup_fsasl_11_11_5_single_func(data, exp_settings, []);

dlmwrite('/home/marcos/Documentos/UFPE/microarray/Experimento/Feature Selection/DataSets/features_scores_by_dataset/GDS183/FSASL_features_score_GDS183.csv',W,'delimiter',';');
