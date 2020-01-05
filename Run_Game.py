from Snake_Game import *
from Feed_Forward_Neural_Network import *
from Feed_Forward_Neural_Network_mousse import *
def get_w(weights):
    return get_weights_from_encoded(weights)
def run_game_with_ML_mov(display, clock, weights):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    steps_per_game = 2500
    score2 = 0
    goback=0

    for _ in range(test_games):
        snake_start, snake_position, apple_position, score = starting_positions()

        count_same_direction = 0
        count_same_direction_mousse=0
        prev_direction = 0
        prev_direction_mousse=0

        for _ in range(steps_per_game):
            goback=0
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(snake_position)
            apple_position, is_front_blocked, is_left_blocked, is_right_blocked, is_back_blocked=blocked_directions_mousse(apple_position)
            angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(snake_position, apple_position)
            predictions = []
            predicted_direction_mousse = np.argmax(np.array(forward_propagation_m_trained(np.array(
                [is_back_blocked,is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 8)))) - 1
            
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1

            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction
           
            if predicted_direction_mousse == prev_direction_mousse:
                count_same_direction_mousse += 1
            else:
                count_same_direction = 0
                prev_direction_mousse = predicted_direction_mousse
                
            new_direction_mousse = [10,0]
            new_direction = np.array(snake_position[0]) - np.array(snake_position[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = generate_button_direction(new_direction)
            button_direction_mousse = generate_button_direction_mousse(new_direction_mousse)

            next_step = snake_position[0] + current_direction_vector
            if collision_with_boundaries(snake_position[0]) == 1 or collision_with_self(next_step.tolist(),
                                                                                        snake_position) == 1:
                score1 += -150
                break
            elif  collision_with_boundaries(apple_position) == 1 :
                goback=1
                
            
            else:
                score1 += 0
            
            
            snake_position, apple_position, score = play_game_mo(goback,snake_start, snake_position, apple_position,
                                                              button_direction_mousse,button_direction, score, display, clock)

            if score > max_score:
                max_score = score

            if count_same_direction > 8 and predicted_direction != 0:
                score2 -= 1
            else:
                score2 += 2


    return score1 + score2 + max_score * 5000

def run_game_with_ML(display, clock, weights):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    steps_per_game = 2500
    score2 = 0

    for _ in range(test_games):
        snake_start, snake_position, apple_position, score = starting_positions()

        count_same_direction = 0
        prev_direction = 0

        for _ in range(steps_per_game):
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
                snake_position)
            angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(
                snake_position, apple_position)
            predictions = []
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1

            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction

            new_direction = np.array(snake_position[0]) - np.array(snake_position[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = generate_button_direction(new_direction)

            next_step = snake_position[0] + current_direction_vector
            if collision_with_boundaries(snake_position[0]) == 1 or collision_with_self(next_step.tolist(),
                                                                                        snake_position) == 1:
                score1 += -150
                break

            else:
                score1 += 0

            snake_position, apple_position, score = play_game(snake_start, snake_position, apple_position,
                                                              button_direction, score, display, clock)

            if score > max_score:
                max_score = score

            if count_same_direction > 8 and predicted_direction != 0:
                score2 -= 1
            else:
                score2 += 2


    return score1 + score2 + max_score * 5000