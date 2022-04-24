# importing libraries
from turtle import distance
import pygame
import time
import random
from math import sqrt
import sys
from pygame.locals import *

snake_speed = 20

# Window size
window_x = 400
window_y = 400

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
purple = pygame.Color(128, 0, 128)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('AI.Snake')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake
# body
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# setting default snake direction
# towards right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0


opposite_direction = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}

secondary_move = {
    'UP': ('LEFT', 'RIGHT'),
    'DOWN': ('LEFT', 'RIGHT'),
    'LEFT': ('UP', 'DOWN'),
    'RIGHT': ('UP', 'DOWN')
}

# displaying Score function


def show_score(choice, color, font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)


# game over function
def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 35)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
    # setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    while(True):
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                pygame.quit()
                quit()


def calculate_distance(snake_x, snake_y):
    return sqrt(pow(snake_x - fruit_position[0], 2) + pow(snake_y - fruit_position[1], 2))


def border_check(move):
    if move == 'UP':
        return snake_position[1] - 10 > 0
    if move == 'DOWN':
        return snake_position[1] + 10 < window_y
    if move == 'LEFT':
        return snake_position[0] - 10 > 0
    if move == 'RIGHT':
        return snake_position[0] + 10 < window_x


def get_next_move_coordinates(move):
    if move == 'UP':
        return snake_position[0], snake_position[1] - 10
    if move == 'DOWN':
        return snake_position[0], snake_position[1] + 10
    if move == 'LEFT':
        return snake_position[0] - 10, snake_position[1]
    if move == 'RIGHT':
        return snake_position[0] + 10, snake_position[1]


def consider_direction(possible_moves):
    lowest = (sys.maxsize, '')

    for move in possible_moves:
        coor = get_next_move_coordinates(move)
        distance = calculate_distance(coor[0], coor[1])
        if distance < lowest[0] and border_check(move):
            lowest = (distance, move)

    return lowest[1]


def is_in_boundary(move, coor):
    if move == 'UP':
        return coor[1] > 0
    elif move == 'DOWN':
        return coor[1] < window_y
    elif move == 'LEFT':
        return coor[0] > 0
    else:
        return coor[0] < window_x


def consider_180_deg_move(possible_moves, change_to):
    possible_moves = secondary_move[change_to]  # UP, DOWN

    lowest = (sys.maxsize, '')

    coor = get_next_move_coordinates(possible_moves[0])
    # distance of first possible move
    distance = calculate_distance(coor[0], coor[1])

    if distance < lowest[0] and is_in_boundary(possible_moves[0], coor):
        lowest = (distance, possible_moves[0])

    coor = get_next_move_coordinates(possible_moves[1])
    # distance of second possible move
    distance = calculate_distance(coor[0], coor[1])

    if distance < lowest[0] and is_in_boundary(possible_moves[1], coor):
        lowest = (distance, possible_moves[1])

    return lowest[1]


def change_direction(change_to):
    global direction

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'


def is_move_180_deg(change_to):
    global direction

    return direction == opposite_direction[change_to]


def is_eating_body(coor):
    next_move = [coor[0], coor[1]]
    if next_move in snake_body:
        return True
    return False


def check_is_eating_body(possible_moves):
    global direction

    if not direction:
        game_over()

    if is_eating_body(get_next_move_coordinates(direction)):
        possible_moves.remove(direction)
        change_to = consider_direction(possible_moves)
        direction = change_to
        check_is_eating_body(possible_moves)


def determine_direction(possible_moves, change_to):
    global direction

    if is_move_180_deg(change_to):
        direction = consider_180_deg_move(possible_moves, change_to)

    change_direction(change_to)
    check_is_eating_body(possible_moves)


def move_snake():
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10


# Main Function
while True:
    pygame.event.get()
    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    change_to = consider_direction(possible_moves)

    determine_direction(possible_moves, change_to)

    move_snake()

    # Snake body growing mechanism
    # if fruits and snakes collide then scores will be
    # incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score countinuously
    show_score(1, white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
