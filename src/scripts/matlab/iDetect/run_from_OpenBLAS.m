% GDS183, GDS1210, GDS4296*, GSE68936, GSE82009, GDS2545

%names = {'GDS183', 'GDS1210', 'GSE68936', 'GSE82009', 'GDS2545'};
names = {'TOX171'}
dataset_location = '/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/featureselectionresearch/Datasets/'
parfor id = 1 : length(names)
	dataset_name = names(id){};

	disp(dataset_name);

	%dataset_name = 'GDS183';

	filename = strcat(dataset_location, dataset_name,'_dataset','.csv');
	dataset = textread(filename,'','delimiter',' ','whitespace','"');
        dataset(:,1) = [];

	dataset = NormalizeFea(dataset);

	exp_settings.it = 20;
	exp_settings.datasetName = dataset_name;

	%% pasta para salvar as parametrizações
	%exp_settings.configFolder = strcat("../config/", dataset_name);

	%% pasta para savar as planilhas de scores das features
	exp_settings.scoreFolder = strcat(pwd,"/rankings/", dataset_name);

	fs_unsup_idetect_single_func(dataset, exp_settings);

end
