## plot graph of features
library(reshape2)
library(dplyr)
library(igraph)

dataset <- read.csv("/home/marcos/projects/Research/featureselectionresearch/PythonWS/UnsFeatureSelection/train_datasets/Carcinom_dataset.csv", sep = " ");
y = dataset$Y;
dataset$Y <- NULL;

# correlation of features
my_cor_matrix <- cor(dataset)

# replace upper triangle of the matrix
# with number that can be used for filtering
my_cor_matrix[upper.tri(my_cor_matrix)] <- 42

#reshape and convert to df
my_cor_df <- melt(my_cor_matrix)

# filter out the upper matrix values
# filter out the self correlations
my_cor_df <- filter(my_cor_df, value != 42) %>% filter(Var1 != Var2)

# create adjacency list with correlations > 0.95
my_adj_list <- my_cor_df %>% filter(value > 0.95)
names(my_adj_list) <- c('from', 'to', 'weight')


###########################################################################
# create igraph S3 object
net <- graph.data.frame(my_adj_list, directed = FALSE)

# store original margins
orig_mar <- par()$mar

# set new margins to limit whitespace in plot
par(mar=rep(.1, 4))

layout <- layout_components(net);
layout <- na.exclude(layout);

# plot graph
plot(net, layout = layout, edge.width = E(net)$weight)
