from Snake_Game import *
from Feed_Forward_Neural_Network_mousse import *
from Feed_Forward_Neural_Network_trained import *
def get_w_m(weights):
    return get_weights_from_encoded_m(weights)
def run_game_with_ML_mousse(display, clock, weights):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    steps_per_game = 2500
    score2 = 0
    print('mousse')

    for _ in range(test_games):
        snake_start, snake_position, apple_position, score = starting_positions()

        count_same_direction = 0
        prev_direction = 0

        for _ in range(steps_per_game):
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
                snake_position)
            apple_position, is_front_blocked, is_left_blocked, is_right_blocked, is_back_blocked=blocked_directions_mousse(apple_position)
            angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(
                snake_position, apple_position)
            
            predictions = []
            predicted_direction = np.argmax(np.array(forward_propagation_m(np.array(
                [is_back_blocked,is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 8), weights))) - 1
            
            predicted_direction_snake = np.argmax(np.array(forward_propagation(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 7)))) - 1
            
            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction

            new_direction = [10,0]
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = generate_button_direction_mousse(new_direction)

            next_step = apple_position + [10,0]
            if collision_with_boundaries(apple_position) == 1 :
                score1 += -150
                break
            elif collision_with_boundaries(snake_position[0]) == 1:
                score1 += 150 
                break

            else:
                score1 += 0
            button_direction=button_direction+10
            snake_position, apple_position, score = play_game_mo(snake_start, snake_position, apple_position,
                                                              button_direction,predicted_direction_snake, score, display, clock)

            if score > max_score:
                max_score = score

            if count_same_direction > 8 and predicted_direction != 0:
                score2 -= 1
            else:
                score2 += 2


    return  score1 +score2 - max_score * 5000