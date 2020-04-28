library(factoextra);
library(latticeExtra);

classes_file_dir = "/home/marcos/projects/Research/featureselectionresearch/PythonWS/UnsFeatureSelection/train_datasets/";
file_dir_name = "/home/marcos/projects/Research/featureselectionresearch/PythonWS/UnsFeatureSelection/results/";
dir_to_save_plots = "/home/marcos/projects/Research/msc/master/images/plots/"

datasets = list("warpAR10P", "warpPIE10P", "ALLAML", "Carcinom", "SMK_CAN", "ProstateGE", "pixraw10P", "TOX171");

#methods = list("LS", "iDetect", "SPEC", "GLSPFS", "Borda_ALL", "Borda_iDetect_GLSPFS", "Borda_LS_GLSPFS", "Borda_LS_IDetect", "Borda_LS_SPEC", "Borda_SPEC_GLSPFS", "Borda_SPEC_iDetect");
methods = list("LS", "iDetect", "SPEC", "GLSPFS",  "Borda_SPEC_iDetect", "Borda_iDetect_GLSPFS");
#methods = list("ALL_Features");

for (dataset_name in datasets) {
  for (method in methods) {
    
    file = paste(file_dir_name, dataset_name, "_after_FS_", method, ".csv", sep = '');
    
    class_file = paste(classes_file_dir, dataset_name,"_dataset.csv", sep = '');
    
    dataset <- read.csv(class_file, sep = " ");
    
    classes <- dataset$Y;
    
    dataset <- read.csv(file, sep = " ");
    #dataset$Y <- NULL;
    
    res_pca <- prcomp(dataset, scale. = TRUE);
    plot_image = paste(dir_to_save_plots, dataset_name, "/", method, ".eps", sep = '');
    
    postscript(plot_image);
    plot <- fviz_pca_ind(res_pca, col.ind = as.factor(classes), legend.title = "Classes", repel = TRUE);
    print(plot)
    dev.off()
  }
}