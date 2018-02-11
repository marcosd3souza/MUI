datasets = list("pixraw10P", "warpPIE10P", "warpAR10P", "ALLAML", "ProstateGE", "TOX171", "SMK_CAN", "Carcinom");

directory_origin = "/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/featureselectionresearch/PythonWS/UnsFeatureSelection/train_datasets/";
directory_dest = "/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/featureselectionresearch/PythonWS/UnsFeatureSelection/train_datasets/filtered/";

for(dataset_name in datasets){
  
  result = c();
  
  ds_file = paste(directory_origin, dataset_name, "_dataset.csv", sep = "");
  dataset = read.csv(ds_file, sep = " ");
  
  Y = dataset$Y;
  
  ds_file = paste(directory_dest, "filtered_", dataset_name, ".csv", sep = "");
  dataset = read.csv(ds_file, sep = " ");
  
  result = cbind(dataset, Y);
  
  write.table(result, file = ds_file, row.names = F);
}
