indexes <- read.csv(file = "/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate/SPEC/GDS183/config_1/evaluate_index.csv", sep = " ");
index_values <- names(indexes[,1:14]);

directory_config <- "/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate";
## SPEC, iDetect, GLSPFS, JELSR
## GDS183, GDS2545, GDS1210, GSE68936, GSE82009

methods <- c("LS", "SparseKMeans", "GLSPFS");
datasets <- c("GDS183", "GDS2545", "GDS1210", "GSE68936", "GSE82009");

for (method in methods) 
{
	for (dataset in datasets) 
	{
		configs_folder <- paste(directory_config, "/", method, "/", dataset, sep="");
		result_files <- dir(configs_folder);

		#criteria <- c("all_features", "second_derivate", "percent", "top");

		criteria_mean <- matrix(,nrow=103, ncol=14);
		criteria_sd <- matrix(,nrow=103, ncol=14);

		values <- c(1:length(result_files)); ## SPEC GDS183
		means <- c(1:14);
		sd_values <- c(1:14);

		print(index_values);

		cont <- 0;

		for(i in 1:103) ## criteria
		{
			for(index in 1:14) ## index value
			{
				for(folder in result_files)
				{
					cont <- cont + 1; 
					config <- paste(configs_folder, "/", folder, "/evaluate_index.csv", sep="");
					indexes <- read.csv(file = config, sep = " ");
					values[cont] <- indexes[i, index];
				}

				cont <- 0;

				means[index] <- mean(values);
				sd_values[index] <- sd(values);
			}

			print(i);
			print(means);
			print(sd_values);

			criteria_mean[i,] <- means;
			criteria_sd[i,] <- sd_values;

		}

		#means
		#sd_values

		#criteria_mean
		#criteria_sd
		colnames(criteria_mean) <- index_values;
		colnames(criteria_sd) <- index_values;

		file_name_result_mean = paste("/home/marcos/Documentos/UFPE/microarray/Experimento/result/result_mean_",method,"_",dataset,".csv", sep="");
		file_name_result_sd = paste("/home/marcos/Documentos/UFPE/microarray/Experimento/result/result_sd_",method,"_",dataset,".csv", sep="");
		write.table(x = criteria_mean, file = file_name_result_mean, row.names = FALSE);
		write.table(x = criteria_sd, file = file_name_result_sd, row.names = FALSE);
	}
}