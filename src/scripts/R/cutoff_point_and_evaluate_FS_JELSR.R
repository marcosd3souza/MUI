
    #### load feature scores data ###########

    ### TIME EXECUTION : 
    #~  7.883921 mins ### METHOD: SPEC; BASE: GDS183; CONFIGS_NON_ZERO: 42
    #~  2.059998 hours ### METHOD: iDetect; BASE: GDS183; CONFIGS_NON_ZERO: 720


    methods = list("JELSR");#, "iDetect", "SPEC", "GLSPFS", "JELSR", "SparseKMeans");
    bases = list("GDS183", "GDS1210");
    scores_folder = "/home/marcos/Documentos/UFPE/microarray/Experimento/scores/";
    datasets_folder = "/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/FeatureSelectionResearch/Datasets/";

    start.time <- Sys.time();

    for(method in methods)
    {
        for(base in bases)
        {
            original_dataset_name = paste(datasets_folder, base, ".csv", sep='');

            original_dataset = read.csv(file = original_dataset_name, header = TRUE);

            evaluate_folder = paste(scores_folder, "evaluate/", sep='');
            dir.create(file.path(evaluate_folder));

            evaluate_folder = paste(evaluate_folder, method, "/", sep='');
            dir.create(file.path(evaluate_folder));

            evaluate_folder = paste(evaluate_folder, base, "/", sep='');
            dir.create(file.path(evaluate_folder));

            score_result_folder = paste(scores_folder, method, "/", "result", "/", base, "/", sep='');

            scores_files = dir(score_result_folder);

            for(file in scores_files)
            {
                    
                scores_filename = paste(score_result_folder, file, sep = '');  
                data <- read.csv(file = scores_filename, header = F);

                if(sum(data) != 0)
                {

                    configuration = paste("config_", strsplit(strsplit(file[1], "_")[[1]][5], ".csv")[[1]][1], sep='');

                    configuration_folder = paste(evaluate_folder, configuration, "/", sep='');
                    dir.create(file.path(configuration_folder));

                    selected_features_by_percent_filename = paste(configuration_folder, "selected_features_by_percent.csv", sep='');
                    seleced_features_by_second_derivate_filename = paste(configuration_folder, "seleced_features_by_second_derivate.csv", sep=''); 
                    second_derivate_image_filename = paste(configuration_folder, "image_features_by_second_derivate.png", sep=''); 


                    #seleced_features_by_second_derivate_filename = "/home/marcos/Documentos/matlab_scripts/selected_features/JELSR/GDS183/second_derivate/selected_features_JELSR_GDS183_config_1_by_2nd_derivate.csv"
                    #second_derivate_image_filename = "/home/marcos/Documentos/matlab_scripts/selected_features/JELSR/GDS183/second_derivate/second_derivate_config_1.png"
                    #seleced_features_by_percent_filename = "/home/marcos/Documentos/matlab_scripts/selected_features/JELSR/GDS183/percent/selected_features_JELSR_GDS183_config_1_by_percent.csv"
                    #evaluation_selected_features_by_derivate_filename = "/home/marcos/Documentos/matlab_scripts/Evaluation/JELSR/GDS183/second_derivate/evaluation_by_second_derivate_config_1.csv"

                    colnames(data) = 'score';

                    feature <- c(1: dim(data)[1]);

                    data <- cbind(data, feature);
                    sorted <- data[order(data[,1], decreasing = TRUE),];

                    NOT_EXISTS_SECOND_DERIVATE = FALSE;
                    NOT_EXISTS_PERCENT = FALSE;

                    #########################################

                    ### calculate 2nd derivate ###
                    len = dim(sorted)[1];
                    second_derivate <- c(1:len);
                    print(len);

                    for(i in 2:len) ## start in second value
                    {

                      if(i+2 <= len)
                      {
                          t1 <- sorted[[1]][i+2] * 1000; ##normalize value
                      }
                      else
                      {
                          t1 <- 0;
                      }

                      if(i+1 <= len)
                      {
                          t2 <- sorted[[1]][i+1] * 1000; ##normalize value
                      }
                      else
                      {
                          t2 <- 0;
                      }

                      second_derivate[[i]] <- abs(t1 + t2 - (2*(sorted[[1]][i] * 1000)));  ## (2_pos_after) + (1_pos_after) - (2 * current_pos)

                    }

                    ### apply cut by 2nd derivate ###

                    ## save image
                    png(second_derivate_image_filename);
                    heading = paste("type=", "l")
                    plot(x=feature[1:30], y=second_derivate[1:30], main=heading);
                    lines(x=feature[1:30], y=second_derivate[1:30], type="l")
                    dev.off();
  

                    #########################################
                    
                     
                    best_value = 0; 
                    for(j in 3:100) ## get top 100 second derivate
                    {
                    	if(second_derivate[j] >= best_value){
                    		best_value = second_derivate[j];

                    		cut_point_by_2nd_derivate = j;
                    	}
                         
                    }

                    if(exists("cut_point_by_2nd_derivate"))
                    {
                        selected_features_by_second_derivate <- sorted[1:cut_point_by_2nd_derivate,2];
                        write.csv(x = selected_features_by_second_derivate, file = seleced_features_by_second_derivate_filename, row.names = F);    
                    }
                    else
                    {
                        NOT_EXISTS_SECOND_DERIVATE = TRUE;
                    }

                    ### calculate percent (50%) ###
                    scores_sum <- sum(sorted[,1]);
                    accumulated = 0;

                    for(r in 1:len)
                    {
                        percent = sorted[r,1]/scores_sum;
                        accumulated = accumulated + percent;

                        if(accumulated >= 0.5)
                        {
                            cut_point_by_percent = r;
                            break;
                        }
                    }

                    if(exists("cut_point_by_percent"))
                    {
                        selected_features_by_percent <- sorted[1:cut_point_by_percent,2];
                        write.csv(x = selected_features_by_percent, file = selected_features_by_percent_filename, row.names = F);    
                    }
                    else
                    {
                        NOT_EXISTS_PERCENT = TRUE;
                    }
                    
                    #### evaluate selected features ####

                    for(top in seq(from=10, to=1000, by=10))
                    {
                        if(exists("features"))
                        {
                            features <- c(features, list(sorted[1:top, 2]));
                        }else
                        {
                            if(NOT_EXISTS_SECOND_DERIVATE && NOT_EXISTS_PERCENT)
                            {
                                features <- list(sorted[,2], sorted[1:top, 2]);
                            }
                            else if(!NOT_EXISTS_SECOND_DERIVATE && NOT_EXISTS_PERCENT)
                            {
                                features <- list(sorted[,2], selected_features_by_second_derivate, sorted[1:top, 2]);
                            }
                            else if(NOT_EXISTS_SECOND_DERIVATE && !NOT_EXISTS_PERCENT)
                            {
                                features <- list(sorted[,2], selected_features_by_percent, sorted[1:top, 2]);
                            }
                            else if(!NOT_EXISTS_SECOND_DERIVATE && !NOT_EXISTS_PERCENT)
                            {
                                features <- list(sorted[,2], selected_features_by_second_derivate, selected_features_by_percent, sorted[1:top, 2]);
                            }
                            
                        }
                    }


                    library(fpc);
                    library(NMI);
                    library(caret);

                    len_features <- length(features);
                    print(len_features);

                    for(index in 1:len_features)
                    {
                        if((len_features == 101 && index > 1) || (len_features == 102 && index > 2) || (len_features == 103 && index > 3))
                        {
                            CRITERIA <- length(features[[index]]);
                        }
                        else if(index == 1)
                        {
                            CRITERIA <- "all_features";
                        }
                        else if(len_features == 102 && index == 2)
                        {
                            if(NOT_EXISTS_PERCENT)
                            {
                                CRITERIA <- "second_derivate";
                            }
                            else
                            {
                                CRITERIA <- "percent";       
                            }
                            
                        }
                        else if(len_features == 103)
                        {
                            if(index == 2)
                            {
                                CRITERIA <- "second_derivate";
                            }
                            else
                            {
                                CRITERIA <- "percent";    
                            }
                            
                        }

                        dataset <- original_dataset[, features[[index]]];
                        features_count <- length(features[[index]]);
                        dgene <- dist(dataset, method = "euclidean");

                        classes_folder <- "/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/FeatureSelectionResearch/classes/";

                        classes_filename = paste(classes_folder, base, "/classes.csv", sep='');

                        #classes_filename <- "/home/marcos/Documentos/UFPE/microarray/Experimento/GIT/FeatureSelectionResearch/classes/GDS183_disease_state_classes.csv";
                        classes <- read.csv(file = classes_filename);

                        k <- max(classes[2]);
                        km <- kmeans(dataset, centers =  k, nstart = 20);

                        stats <- cluster.stats(dgene, km$cluster, alt.clustering = as.integer(classes$label), G2 = TRUE, G3 = TRUE);                    

                        mat <- matrix(stats, byrow = TRUE, ncol = 34);

                        colnames(mat) <- names(stats);

                        values <- mat[,c(22,23,24,25,26,27,29,32,33,34)];

                        index_values <- matrix(values, byrow = T, ncol = 10);

                        colnames(index_values) <- names(values);

                        ## inclusão do NMI
                        x_classes <- classes[,1:2];
                        y_kmeans <- cbind(c(1:dim(classes)[1]), km$cluster);
                        nmi <- NMI(x_classes, y_kmeans);

                        index_values <- cbind(index_values, nmi);
                        ##

                        ## inclusão da acurácia
                        truth <- classes[,2];
                        predict <- km$cluster;
                        confusion_matrix <- confusionMatrix(truth, predict);
                        accuracy <- confusion_matrix$overall[[1]];

                        index_values <- cbind(index_values, accuracy);
                        ##

                        ## f-measure pra cluster
                        tb <- na.omit(as.data.frame(confusion_matrix$byClass));

                        verify <- rowSums(tb, na.rm = T);

                        if(length(verify) != 0 && sum(tb$Precision) != 0 && sum(tb$Recall) != 0)
                        {

                        	f_measure_mean <- 2 * mean(tb$Precision) * mean(tb$Recall) / (mean(tb$Precision) + mean(tb$Recall));
                        	f_measure_sum <- 2 * sum(tb$Precision) * sum(tb$Recall) / (sum(tb$Precision) + sum(tb$Recall));
                        }
                        else
                        {
                        	f_measure_mean <- 0;
                        	f_measure_sum <- 0;
                        }

                        

                        index_values <- cbind(index_values, f_measure_mean);
                        index_values <- cbind(index_values, f_measure_sum);
                        ##    

                        index_values <- cbind(index_values, CRITERIA);
                        index_values <- cbind(index_values, features_count);

                        if(exists("evaluate_index"))
                        {
                            evaluate_index <- rbind(evaluate_index, index_values);
                        }
                        else
                        {
                            evaluate_index <- index_values;
                        }
                    }
                    
                    result_filename = paste(configuration_folder, "evaluate_index.csv", sep='');
                    write.table(x = evaluate_index, file = result_filename, row.names = FALSE);

                    rm(evaluate_index);
                    rm(features);
                }
            }

        }

    }

    end.time <- Sys.time()

    time.taken <- end.time - start.time

    print("total time: ");
    time.taken
    

    

    

    



