
datasets <- c("GDS183", "GDS2545", "GDS1210", "GSE68936", "GSE82009");
methods <- c("GLSPFS","SparseKMeans","LS","iDetect","SPEC");
evaluation <- c("nmi","corrected.rand","f_measure_mean","dunn","accuracy");

for (evaluation_index in evaluation) 
{

	for (dataset in datasets) 
	{
		for (method in methods) 
		{
			config_folder <- paste("/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate/",method,"/", dataset, "/", sep = "");
			configs <- dir(config_folder);

			print(config_folder)

			results <- matrix(,nrow=length(configs), ncol=103);
			cont <- 0;

			for(config in configs)
			{
			  file_name <- paste(config_folder, config, "/evaluate_index.csv", sep = "");
			  data <- read.csv(file_name, sep = " ");

			  results[cont,] <- data[,evaluation_index];

			  cont <- cont + 1;
			}

			colnames(results) <- data$CRITERIA;

			folder_result = paste("/home/marcos/Documentos/UFPE/microarray/Experimento/result/",dataset,"/", method,"/",sep="");

			if(!dir.exists(folder_result))
			{
				dir.create(folder_result, recursive = T);
			}

			result_file_name = paste(folder_result, evaluation_index,".csv",sep="");

			write.table(x = results, file = result_file_name, row.names = FALSE);

		}

	}

}
