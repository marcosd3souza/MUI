% GDS183, GDS1210, GDS4296*, GSE68936, GSE82009, GDS2545
names = {'GDS183', 'GDS1210', 'GSE68936', 'GSE82009', 'GDS2545'};

parfor id = 1 : length(names)

	dataset_name = names(id){};

	filename = strcat('/home/marcos/Documentos/matlab_scripts/datasets/', dataset_name,'.csv');
	dataset = textread(filename,'','delimiter',',','whitespace','"');

	fea = NormalizeFea(dataset);

	W = constructW(fea);

	LaplacianScore = LaplacianScore(fea, W);

        result_file_name = strcat("/home/marcos/Documentos/matlab_scripts/scores/LS/result/", dataset_name)
	dlmwrite(result_file_name, LaplacianScore);
end
