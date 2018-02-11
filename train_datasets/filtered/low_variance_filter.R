vars = c();
datasets = list("pixraw10P", "warpPIE10P", "warpAR10P", "ALLAML", "ProstateGE", "TOX171", "SMK_CAN", "Carcinom");

direrctory = "/home/marcos/Documentos/UFPE/microarray/Experimento/normalized_datasets/";

for(dataset_name in datasets){
  ds_file = paste(direrctory, "result_", dataset_name, "_normalized.csv", sep = "");
  dataset = read.csv(ds_file, sep = " ");
  dataset$X = NULL;
  n_fea = length(dataset)[1];

  vars = c();
  
  for(feature in names(dataset)) {
    vars = rbind(vars, var(dataset[, feature]));
  }
  
  vars = cbind(c(1:n_fea), vars);
  ordered_features = vars[order(vars[,2], decreasing = T),][,1];
  
  cut_off = as.integer(0.75 * length(ordered_features));
  selected  = ordered_features[1:cut_off];
  
  filtered = dataset[, selected];
  
  result_file_name = paste("/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/featureselectionresearch/PythonWS/UnsFeatureSelection/train_datasets/filtered/filtered_", dataset_name, ".csv", sep="");
  write.table(filtered, file = result_file_name, row.names = F);
}
