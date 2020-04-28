class InitialValues:

    def __init__(self,
                 cutoff_methods,
                 best_config,
                 n_iter,
                 best_cutoff_method,
                 best_silhouette,
                 initial_best_metric,
                 state_of_art):

        self.state_of_art = state_of_art

        self.cutoff_methods = cutoff_methods
        self.best_config = best_config
        self.n_iter = n_iter
        self.best_cutoff_method = best_cutoff_method
        self.best_silhouette = best_silhouette
        self.initial_best_metric = initial_best_metric
