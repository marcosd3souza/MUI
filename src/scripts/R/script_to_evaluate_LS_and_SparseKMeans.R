#/home/marcos/Documentos/UFPE/microarray/Experimento/result/GDS2545/mean_and_sd/result_mean_LS_GDS2545.csv

datasets_names <- c("GDS183", "GDS1210", "GDS2545", "GSE68936", "GSE82009");
methods <- c("LS", "SparseKMeans");
avaliations <- c("accuracy", "dunn", "f_measure_mean", "nmi", "corrected.rand");

directory = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/";
col_names <- c("all_features", "second_derivate", "percent", seq(from = 10, to = 1000, by = 10));

data_result <- read.csv(file = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/final_result_compiled.csv", sep = " ", stringsAsFactors = FALSE);

for(dataset in datasets_names){
  for(method in methods){
   file_name <- paste(directory, dataset, "/mean_and_sd/", "result_mean_", method , "_", dataset, ".csv", sep = "");
   raw_dataset <- read.csv(file_name, sep = " ");
   
   dataset_res <- raw_dataset[, avaliations];
   
   for(avaliation in avaliations){
     
     pos <- which(dataset_res[,avaliation] == max(dataset_res[,avaliation]))[1]
     value_cutoff <- col_names[pos];
     new_row <- c(avaliation, value_cutoff, dataset, method);
     
     data_result[nrow(data_result)+1,] <- new_row;
     
   }
  }
}

