from models.initial_values import InitialValues
from common.commons import Cutoff, get_cutoff_magic_numbers


def get_initial_variables(is_default_values):

    # cutoff_methods = presets.get_cutoff_magic_numbers(10, 210, 10)
    # cutoff_methods = [top for top in get_cutoff_magic_numbers()]

    if is_default_values:
        cutoff_methods = [top for top in get_cutoff_magic_numbers()]
    else:
        cutoff_methods = [Cutoff.INFLEXION.name]

    # if not state_of_art:
        # cutoff_methods.append(Cutoff.INFLEXION.name)
        # cutoff_methods.append(Cutoff.QUARTILE_1.name)
        # cutoff_methods.append(Cutoff.QUARTILE_2.name)
        # cutoff_methods.append(Cutoff.QUARTILE_3.name)

    best_cutoff_method = ""

    # avg silhouette
    best_silhouette = -1

    best_config = -1
    n_iter = 1
    initial_best_metric = 0

    return InitialValues(cutoff_methods,
                         best_config, n_iter,
                         best_cutoff_method,
                         best_silhouette,
                         initial_best_metric,
                         is_default_values)
