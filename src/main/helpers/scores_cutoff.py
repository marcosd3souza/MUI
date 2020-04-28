import math

# from rpy2.robjects.packages import importr
# stats = importr('stats')
from numba import jit


def calculate_second_derivate(scores):
    second_derivate = []

    n_rows = scores.shape[0]

    for index in range(0, n_rows):
        #second_derivate.append(item)
        if index > 0 and index < n_rows-1:
            
            if index + 1 < n_rows:
                first_term = scores.iat[index + 1, 0]  # normalize value
            else:
                break

            if index + 2 < n_rows :
                second_term = scores.iat[index + 2, 0]  # normalize value
            else:
                break
            
            # (1_pos_after) + (2_pos_after) - (2 * current_pos)
            current_result = math.fabs(first_term + second_term - (2 * scores.iat[index, 0]))
            second_derivate.append(current_result)
            
    return second_derivate


def get_cut_off_point_by_second_derivate(values_sorted, minimum=2):
    derivate_values = calculate_second_derivate(values_sorted)

    position = 0
    bestValue = 0
    # first derived is the second item, but indexes starting with 0, so the first is 1
    index = 1
    for value in derivate_values:
        if index > minimum and value > bestValue:
            bestValue = value
            position = index
        index = index + 1

    return position


def get_point_by_inflexion(values):
    values_sorted = values.sort_values(by="values",  ascending=False)
    result = get_cut_off_point_by_second_derivate(values_sorted)

    return result


def get_cut_off_point_by_percent(scores, percent_threshold):
    scores_sum = sum(scores.values)
    n_rows = scores.shape[0]
    position = 0
    accumulated_percent = 0
    
    for i in range(0, n_rows):
        
        current_percent = scores.iat[i, 0] / scores_sum
        accumulated_percent = accumulated_percent + current_percent
        
        if accumulated_percent >= percent_threshold:
            position = i+1
            break
    
    return position


def get_cut_off_point_by_quartile(scores, q):
    position = 0
    quartile = 0
    n_rows = scores.shape[0]

    if q == 1:  # first quartile
        quartile = float(scores.score.quantile([0.25]))
    elif q == 2:  # second quartile
        quartile = float(scores.score.quantile([0.50]))
    elif q == 3:  # third quartile
        quartile = float(scores.score.quantile([0.75]))

    for i in range(0, n_rows):
        if scores.iat[i, 0] <= quartile:
            position = i-1
            break

    return position
