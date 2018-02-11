import math

def calculate_second_derivate(scores):
    second_derivate = []

    n_rows = scores.shape[0]

    for index in range(0, n_rows):
        #second_derivate.append(item)
        if index > 1 and index < n_rows-2:
            
            if index + 1 < n_rows:
                first_term = scores.iat[index + 1, 0]  # normalize value
            else:
                first_term = 0

            if index + 2 < n_rows :
                second_term = scores.iat[index + 2, 0]  # normalize value
            else:
                second_term = 0
            
            # (1_pos_after) + (2_pos_after) - (2 * current_pos)
            current_result = math.fabs(first_term + second_term - (2 * scores.iat[index, 0]));
            second_derivate.append(current_result);
            
    return second_derivate

def get_cut_off_point_by_second_derivate(scores):
    derivate_values = calculate_second_derivate(scores);
    
    position = 0;
    bestValue = 0;
    index = 3;
    for value in derivate_values:
        index = index + 1;
        if value > bestValue:
            bestValue = value
            position = index;
            
    return position;

def get_cut_off_point_by_percent(scores):
    scores_sum = sum(scores.values);
    n_rows = scores.shape[0];
    position = 0;
    accumulated_percent = 0;
    
    for i in range(0, n_rows):
        
        current_percent = scores.iat[i, 0] / scores_sum;
        accumulated_percent = accumulated_percent + current_percent;
        
        if accumulated_percent >= 0.5:
            position = i+1;
            break;
    
    return position;        
      
