import random
import random
import time
import math
from tqdm import tqdm
import numpy as np
import pygame
import timeit

def display_snake(snake_position, display):
    for position in snake_position:
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(position[0], position[1], 10, 10))


def display_apple(apple_position, display):
    
    pygame.draw.rect(display, (0, 255, 0), pygame.Rect(apple_position[0], apple_position[1], 10, 10))
    


def starting_positions():
    snake_start = [100, 100]
    snake_position = [[100, 100], [90, 100], [80, 100]]
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score = 0

    return snake_start, snake_position, apple_position, score


def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))

def generate_mousse( apple_position,button_direction):
    
    if  button_direction == 1 : 
        apple_position[0]=apple_position[0]+10
            
    elif button_direction== 0: 
        apple_position[0]=apple_position[0]-10
            
    elif button_direction==2 : 
        apple_position[1]=apple_position[1]+10
    else :
        apple_position[1]=apple_position[1]-10
    
    return apple_position
def goback(snake_start): 
    if snake_start[0] >= 500:
        snake_start[0] = random.randrange(1, 50) * 10
    elif  snake_start[0] < 0 :
        snake_start[0] = random.randrange(1, 50) * 10
    elif  snake_start[1] >= 500:
        snake_start[1] = random.randrange(1, 50) * 10
    else : 
        snake_start[1] = random.randrange(1, 50) * 10 
    return snake_start
    
    
def generate_snake(snake_start, snake_position, apple_position, button_direction, score):
    if button_direction == 1:
        snake_start[0] += 10
    elif button_direction == 0:
        snake_start[0] -= 10
    elif button_direction == 2:
        snake_start[1] += 10
    else:
        snake_start[1] -= 10

    if snake_start == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_start))

    else:
        snake_position.insert(0, list(snake_start))
        snake_position.pop()

    return snake_position, apple_position, score


def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score
def mousse_limites (apple_position): 
    if apple_position[0] >= 500 or apple_position[0] < 0 or apple_position[1] >= 500 or apple_position[1] < 0:
        return 1
    else:
        return 0 


def collision_with_boundaries(snake_start):
    if snake_start[0] >= 500 or snake_start[0] < 0 or snake_start[1] >= 500 or snake_start[1] < 0:
        return 1
    else:
        return 0


def collision_with_self(snake_start, snake_position):
    # snake_start = snake_position[0]
    if snake_start in snake_position[1:]:
        return 1
    else:
        return 0
def blocked_directions_mousse(apple_position):
    is_front_blocked = is_direction_blocked_mousse(apple_position, [10,0])
    is_left_blocked = is_direction_blocked_mousse(apple_position, [0,-10])
    is_right_blocked = is_direction_blocked_mousse(apple_position, [0,10])
    is_back_blocked =  is_direction_blocked_mousse(apple_position, [-10,0])

    return apple_position, is_front_blocked, is_left_blocked, is_right_blocked, is_back_blocked



def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])
    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

def is_direction_blocked_mousse(snake_position, current_direction_vector):
    next_step = snake_position + current_direction_vector
    snake_start = snake_position
    if collision_with_boundaries(next_step) == 1 :
        return 1
    else:
        return 0

def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    snake_start = snake_position[0]
    if collision_with_boundaries(next_step) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
        return 1
    else:
        return 0


def generate_random_direction(snake_position, angle_with_apple):
    direction = 0
    if angle_with_apple > 0:
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    else:
        direction = 0

    return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector

    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction


def direction_vector_mousse(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector

    if direction == -1:
        new_direction =right_direction_vector 
    if direction == 1:
        new_direction = left_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction
def generate_button_direction_mousse(new_direction):
    button_direction = 0
    if new_direction[0] ==10 and new_direction[1]==0 :
        button_direction = 1
    elif new_direction[0] ==-10 and new_direction[1]==0 :
        button_direction = 0
    elif new_direction[0] ==0 and new_direction[1]==10 :
        button_direction = 2
    else:
        button_direction = 3

    return button_direction
    

def generate_button_direction(new_direction):
    button_direction = 0
    if new_direction.tolist() == [10, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-10, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, 10]:
        button_direction = 2
    else:
        button_direction = 3

    return button_direction

def vectornor(appel_position):
    norm_of_appl = np.linalg.norm(appel_position)
    appel_position=appel_position /norm_of_appl
    return appel_position
    

def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized


def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill((255, 255, 255))
        
        display_apple(apple_position, display)
        
        display_snake(snake_position, display)
        
           
        snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
                                                               button_direction, score)
        pygame.display.update()
        clock.tick(5000)

        return snake_position, apple_position, score

def play_game_mo(back,snake_start, snake_position, apple_position, button_direction,predicted_direction_snake, score, display, clock):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill((255, 255, 255))
        
        display_apple(apple_position, display)
        
        display_snake(snake_position, display)
        if back : 
            appel_position=goback(apple_position)
            snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
                                                               predicted_direction_snake, score)
        else :

            
            apple_position=generate_mousse( apple_position,button_direction)
            snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
                                                               predicted_direction_snake, score)
        
        pygame.display.update()
        clock.tick(5000)

        return snake_position, apple_position, score

'''
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN ->button_direction = 2
UP -> button_direction = 3
'''

display_width = 500
display_height = 500
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()
display=pygame.display.set_mode((display_width,display_height))
clock=pygame.time.Clock()