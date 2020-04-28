datasets_names <- c("GDS183", "GDS1210", "GDS2545", "GSE68936", "GSE82009");
methods <- c("GLSPFS", "iDetect", "SPEC");
avaliations <- c("accuracy", "dunn", "f_measure_mean", "nmi", "corrected.rand");

data_transformed <- data.frame();

directory = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/";

for (dataset_name in datasets_names) {
  for (method in methods) {
    for (avaliation in avaliations) {
      file_name <- paste(directory,dataset_name,"/",method,"/",avaliation,".csv", sep = "");
      
      data <- read.csv(file = file_name, sep = " ");
      data <- na.omit(data);

      ordered_cols_means <- sort(colMeans(data), decreasing = T);

      data <- data[, names(ordered_cols_means)];

      ordered_cols_means_file_name <- paste(directory, dataset_name,"_",method,"_",avaliation,"_ordered_means.txt", sep = "");

      write(names(ordered_cols_means), file = ordered_cols_means_file_name);
      
      for (id in 1:103) {
        v <- data[, id];
        for(i in 1:length(v)){names(v)[i] = id}
        
        criteria <- data.frame(names(v), v);
        
        colnames(criteria) <- c("criteria", "value");
        
        data_transformed <- rbind(data_transformed, criteria);
      }
      
      file_to_save = paste(directory, dataset_name,"_",method,"_",avaliation,"_compiled.csv", sep = "");
      write.table(data_transformed, file = file_to_save, row.names = F);
      
      data_transformed <- data.frame();
    }
  }
}