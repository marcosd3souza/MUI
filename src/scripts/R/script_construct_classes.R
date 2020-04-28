## get GDS/GSE
geo <- getGEO(GEO = "GDS183");
# geo <- getGEO(GEO = "GSE68936", AnnotGPL = T);
# data <- pData(geo$GSE68936_series_matrix.txt.gz)[,c(2,11)];

## convert to Table
geo_data <- dataTable(geo);
samples <- Columns(geo_data);

## create classes object
classes <- c(1:40);
#classes <- cbind(classes, as.integer(data[,2]));
classes <- cbind(classes, as.integer(samples[,2]));
colnames(classes)[1] = "sample";
colnames(classes)[2] = "disease_state";
#sample_description <- data[,1];
#tissue_description <- data[,2];
sample_description <- samples[,1];
disease_state_description <- samples[,2];
classes <- cbind(classes, as.data.frame.character(sample_description));
classes <- cbind(classes, as.data.frame.character(disease_state_description));

## save
write.csv(x = classes, file = "/home/marcos/Documentos/matlab_scripts/GIT/FeatureSelectionResearch/classes/GDS183_disease_state_classes.csv", row.names = F);




