# Unsupervised Feature Selection Methodology for Clustering in High Dimensionality Datasets
Research project to perform feature selection in unsupervised learning

# Abstract

Feature selection is an important research area that seeks to eliminate unwanted features from datasets. Many feature selection methods are suggested in the literature, but the evaluation of the best set of features is usually performed using supervised metrics, where labels are required. In this work we propose a methodology that tries to aid data specialists to answer simple but important questions, such as: (1) do current feature selection methods give similar results? (2) is there is a consistently better method ? (3) how to select the m-best features? (4) as the methods are not parameter-free, how to choose the best parameters in the unsupervised scenario? and (5) given different options of selection, could we get better results if we fusion the results of the methods? If yes, how can we combine the results? We analyze these issues and propose a methodology that, based on some unsupervised methods, will make feature selection using strategies that turn the execution of the process fully automatic and unsupervised, in high-dimensional datasets. After, we evaluate the obtained results, when we see that they are better than those obtained by using the selection methods at standard configurations. In the end, we also list some further improvements that can be made in future works.

# Pre-Conditions
It's necessary install some packages/softwares before execution:

- Octave GNU Linux
- Scikit-learn (package to execute K-Means)
- oct2py (package to execute octave code)
- Anaconda 1.6+

# Reference
https://seer.ufrgs.br/rita/article/view/RITA_VOL27_NR2_30