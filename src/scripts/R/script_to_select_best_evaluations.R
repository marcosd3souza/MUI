datasets_names <- c("GDS183", "GDS1210", "GDS2545", "GSE68936", "GSE82009");
methods <- c("GLSPFS", "iDetect", "SPEC");
evaluations <- c("accuracy", "dunn", "f_measure_mean", "nmi", "corrected_rand");

v_n_features <- c(3036, 7122, 12558, 7129, 12625);

index <- 0;
best_evaluation <- 0;
config_of_best_evaluation <- 0;

best_results <- data.frame();

column_names <- c("dataset", "n_features", "method", "evaluation",
                  "best_cut_point","eval_to_all_features", 
                  "eval_to_best_cut_point", "best_config");

directory = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/";

#/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate/   GLSPFS/GDS183/config_165/seleced_features_by_second_derivate.csv
#/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate/   GLSPFS/GDS183/config_165/selected_features_by_percent.csv

scores_evaluated <- "/home/marcos/Documentos/UFPE/microarray/Experimento/scores/evaluate/";

for (dataset_name in datasets_names) {
  index <- index + 1;
  
  n_features <- v_n_features[index];
  
  for (method in methods) {
    
    for (evaluation in evaluations) {
      
      file_name <- paste(directory, dataset_name, "/", method, "/", evaluation, "/", evaluation,".csv", sep = "");
      
      data <- read.csv(file = file_name, sep = " ");
      data <- na.omit(data);
      
      eval_to_all_features <- max(data[,1]);
      
      for(i in 1:103){
        
        current_value <- max(data[,i]);
        current_config <- which.max(data[,i]);
        
        if(current_value > best_evaluation){
          best_evaluation <- current_value;
          config_of_best_evaluation <- current_config;
          cut_point <- names(data)[i];
          
          if(cut_point == "second_derivate"){
            file <- paste(scores_evaluated, "/", method, "/", dataset_name, "/", "config_", config_of_best_evaluation, "/seleced_features_by_second_derivate.csv", sep = "");
            selected_by_derivate <- read.csv(file);
            
            len_by_derivate <- length(selected_by_derivate[,1]);
            
            cut_point <- paste(cut_point, "_top_", len_by_derivate, sep = "");
          }else if(cut_point == "percent"){
            
            file <- paste(scores_evaluated, "/", method, "/", dataset_name, "/", "config_", config_of_best_evaluation, "/selected_features_by_percent.csv", sep = "");
            selected_by_percent <- read.csv(file);
            
            len_by_percent <- length(selected_by_percent[,1]);
            
            cut_point <- paste(cut_point, "_top_", len_by_percent, sep = "");
          }
        }
        
      }
      
      current_row <- data.frame(dataset_name, n_features, method, evaluation, 
                                cut_point, eval_to_all_features, best_evaluation, 
                                config_of_best_evaluation);
      
      colnames(current_row) <- column_names;
      
      best_results <- rbind(best_results, current_row);
      
      best_evaluation <- 0;
      config_of_best_evaluation <- 0;
    }
    
  }
}