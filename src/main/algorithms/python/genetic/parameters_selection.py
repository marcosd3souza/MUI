import random
import numpy as np

from helpers import logger
from oct2py import octave


def select_best_rankings(n_features, population, method,
                         data=None,
                         fit_func=None,
                         construct_w_func=None,
                         state_of_art=False):

    if method == 'iDetect':
        octave.addpath("algorithms/matlab")
    elif method == 'GLSPFS':
        octave.addpath("algorithms/matlab/GLSPFS")

    if state_of_art:
        number_of_solutions = 1
        number_of_generations = 1
        new_population = range(1)
    else:
        initial_population_size = 50
        number_of_solutions = 10
        number_of_generations = 5
        new_population = random.sample(range(len(population)), initial_population_size)

    scores = np.empty([n_features, 1])
    scores[:, 0] = None

    logger.log("full population : " + str(len(population)), True)

    for gen in range(number_of_generations):

        logger.log("generation : " + str(gen), True)

        fitness = []

        for i in new_population:

            rank = get_method_rank(method, construct_w_func, fit_func, population[i], n_features, data)

            if sum(rank) == 0:
                continue

            fitness.append(np.std(rank))

        if not state_of_art:
            parents, children = select_mating_pool(population, new_population, fitness,  number_of_solutions)

            if gen + 1 == number_of_generations:

                for param in parents:
                    rank = get_method_rank(method, construct_w_func, fit_func, param, n_features, data)
                    rank = rank.reshape((rank.shape[0], 1))
                    scores = np.append(scores, rank, 1)
            else:
                # Generating next generation using crossover with parents.
                offspring_crossover_parents = crossover(parents, number_of_solutions)

                # Adding some variations to the offsrping using mutation.
                offspring_crossover_mutation_parents = mutation(offspring_crossover_parents)

                # Creating the new population based on the parents and origin.
                new_population = []
                import more_itertools as mit
                new_population[0:len(parents)] = list(
                    mit.locate(population, pred=lambda p: p in parents)
                )

                new_population[len(parents):len(offspring_crossover_parents)] = list(
                    mit.locate(population, pred=lambda p: p in offspring_crossover_parents)
                )

                new_population[len(offspring_crossover_parents):len(offspring_crossover_mutation_parents)] = list(
                    mit.locate(population, pred=lambda p: p in offspring_crossover_mutation_parents)
                )

                if len(children) > 0:
                    # Generating next generation using crossover with children.
                    offspring_crossover_children = crossover(children, number_of_solutions)

                    # Adding some variations to the offsrping using children.
                    offspring_crossover_mutation_children = mutation(offspring_crossover_children)

                    new_population[len(offspring_crossover_mutation_parents):len(offspring_crossover_children)] = list(
                        mit.locate(population, pred=lambda p: p in offspring_crossover_children)
                    )

                    new_population[
                    len(offspring_crossover_children):len(offspring_crossover_mutation_children)] = list(
                        mit.locate(population, pred=lambda p: p in offspring_crossover_mutation_children)
                    )

                print("new generation size: " + str(len(new_population)))

    return scores[:, 1:]


def get_method_rank(method, construct_w_func, fit_func, params, n_features=None, data=None):
    rank = None
    if method == 'SPEC':
        rank = compute_ranking_to_spec(construct_w_func, fit_func, params)
    elif method == 'LS':
        rank = compute_ranking_to_ls(construct_w_func, fit_func, params)
    elif method == 'iDetect':
        rank = octave.iDetect(data, params)
    elif method == 'GLSPFS':
        rank = compute_ranking_to_glspfs(data, params, n_features)

    return rank


def compute_ranking_to_ls(construct_w_func, fit_func, params):
    W = construct_w_func(params)

    LS_args = {'W': W}
    return fit_func(LS_args)


def compute_ranking_to_spec(construct_w_func, fit_func, params):
    w = construct_w_func(params)
    style = params["style"]

    spec_args = {'style': style, 'W': w}
    return fit_func(spec_args)


def compute_ranking_to_glspfs(data, params, n_features):
    K = octave.constructKernel(data, data, params["global_kernel_option"])
    L = octave.computeLocalStructure(data, params["local_type"],
                                     params["local_k"],
                                     params["local_lpp_sigma"],
                                     params["local_ltsa_embedded_dim"])

    rank = octave.fs_unsup_glspfs(data, K, L, params["lambda1"], params["lambda2"], n_features)
    return rank


def select_mating_pool(pop, origin, fitness, num_parents):

    # Selecting the best individuals in the current generation as parents
    #  for producing the offspring of the next generation.

    selected_individual_value = -99999999999
    parents = []
    children = []

    for parent_num in range(num_parents):

        max_fitness_idx = np.where(fitness == np.max(fitness))

        max_fitness_idx = max_fitness_idx[0][0]

        parents.append(pop[origin[max_fitness_idx]])

        fitness[max_fitness_idx] = selected_individual_value

    idx_others = np.where(fitness != np.unique(selected_individual_value))[0]
    for idx in idx_others:
        children.append(pop[origin[idx]])

    return parents, children


def crossover(parents, offspring_size):
    offspring = []
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = np.uint8(len(parents[0]) / 2)

    for k in range(offspring_size):
        # Index of the first parent to mate.
        parent1_idx = k % len(parents[0])
        # Index of the second parent to mate.
        parent2_idx = (k + 1) % len(parents[0])
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring.append(dict(
            np.concatenate(
                [
                np.array(list(parents[parent1_idx].items())[0:crossover_point], dtype=object),
                np.array(list(parents[parent2_idx].items())[crossover_point:], dtype=object)
                ]
            )
        )
        )
    return offspring


def mutation(offspring_crossover):

    # Mutation changes a single gene in each offspring randomly.

    for idx in range(len(offspring_crossover)):

        # The random value to be added to the gene.
        random_k_value = random.sample(range(3, 20, 2), 1)[0]
        random_t_value = random.sample(range(1, 10, 2), 1)[0]

        offspring_crossover[idx]["k"] = random_k_value
        offspring_crossover[idx]["t"] = random_t_value

    return offspring_crossover
