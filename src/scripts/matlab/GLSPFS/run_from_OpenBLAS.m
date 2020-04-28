% GDS183, GDS1210, GDS4296*, GSE68936, GSE82009, GDS2545

names = {'GDS183', 'GDS1210', 'GSE68936', 'GSE82009', 'GDS2545'};

parfor id = 1 : length(names)
	dataset_name = names(id){};

	disp(dataset_name);

	filename = strcat('/home/marcos/Documentos/matlab_scripts/datasets/', dataset_name,'.csv');
	dataset = textread(filename,'','delimiter',',','whitespace','"');

	dataset = NormalizeFea(dataset);

	exp_settings.FeaNumCandi = size(dataset,2);
	exp_settings.nKmeans = 5;
	exp_settings.datasetName = dataset_name;

	%% pasta para salvar as parametrizações
	exp_settings.configFolder = strcat("/home/marcos/Documentos/matlab_scripts/scores/GLSPFS/config/", dataset_name);

	%% pasta para savar as planilhas de scores das features
	exp_settings.scoreFolder = strcat("/home/marcos/Documentos/matlab_scripts/scores/GLSPFS/result/", dataset_name);

	fs_unsup_glspfs_single_func(dataset, exp_settings, []);
end
