
#"/home/marcos/Documentos/UFPE/microarray/Experimento/result/GDS2545/iDetect/f_measure/GDS2545_iDetect_f_measure_mean_compiled.csv";

datasets_names <- c("GDS183", "GDS1210", "GDS2545", "GSE68936", "GSE82009");
methods <- c("GLSPFS", "iDetect", "SPEC");
avaliations <- c("accuracy", "dunn", "f_measure_mean", "nmi", "corrected_rand");

directory = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/";

extend <- function(alphabet) function(i) {
  base10toA <- function(n, A) {
    stopifnot(n >= 0L)
    N <- length(A)
    j <- n %/% N 
    if (j == 0L) A[n + 1L] else paste0(Recall(j - 1L, A), A[n %% N + 1L])
  }   
  vapply(i-1L, base10toA, character(1L), alphabet)
}

generate_letters <- extend(letters);

data_result <- data.frame(matrix(ncol = 4, nrow = 0), stringsAsFactors = FALSE);
colnames(data_result) <- c("avaliation", "cutoff", "dataset", "method");

for(dataset in datasets_names){
  
  print(paste("dataset: ", dataset, sep = ""));
  
  for(method in methods){
    
    print(paste("method: ", method, sep = ""));
    
    for(avaliation in avaliations){
      
      print(paste("avaliation: ", avaliation, sep = ""));
      
      ordered_means_filename <- paste(dataset, "_", method, "_", avaliation, "_ordered_means.txt",sep = "");
      ordered_filename <- paste(directory, dataset, "/", method,"/", avaliation,"/", ordered_means_filename, sep = "");
      
      ordered_means <- read.csv(file = ordered_filename, sep = " ", header = F);
      
      compiled_result_filename <- paste(dataset, "_", method, "_", avaliation, "_compiled.csv",sep = "");
      avaliation_result_filename <- paste(directory, dataset, "/", method,"/", avaliation,"/",compiled_result_filename, sep = "");
      data <- read.csv(file = avaliation_result_filename, sep = " ");
      
      data[,1] <- generate_letters(data[,1]);
      
      model=lm( data$value ~ data$criteria);
      ANOVA=aov(model);
      TUKEY <- TukeyHSD(x=ANOVA, 'data$criteria', conf.level=0.95);
      
      tukey_result_all <- data.frame(TUKEY$'data$criteria');
      tukey_result_all[tukey_result_all$p.adj>0.05,] <- NA;
      
      tukey_result_na <- na.omit(tukey_result_all);
      
      position <- match(strsplit(rownames(tukey_result_na[1,]),"-")[[1]][2],generate_letters(c(1:103)));
      
      value_cutoff <- as.character(ordered_means[position, 1]);
      
      new_row <- c(avaliation, value_cutoff, dataset, method);
      
      data_result[nrow(data_result)+1,] <- new_row; 
    }
  }
}

write.table(data_result, file = "/home/marcos/Documentos/UFPE/microarray/Experimento/result/final_result_compiled.csv");












