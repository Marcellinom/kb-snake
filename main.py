# import library
from turtle import distance
import pygame
import time
import random
from math import sqrt
import sys
from pygame.locals import *

# Pembuatan dan Settingan Object Game
# Ukuran Window
window_x = 400
window_y = 400

# RGB
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
purple = pygame.Color(128, 0, 128)

# Init pygame
pygame.init()

# Setting dari Window
pygame.display.set_caption('AI.Snake')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# Posisi awal snake
snake_speed = 20
snake_position = [100, 50]

# Posisi 4 block ular
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]]

# Posisi fruit
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# setting arah gerak awal snake
direction = 'RIGHT'
change_to = direction

# Arah berlawanan
opposite_direction = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}

# Arah yang mungkin untuk setiap arah
secondary_move = {
    'UP': ('LEFT', 'RIGHT'),
    'DOWN': ('LEFT', 'RIGHT'),
    'LEFT': ('UP', 'DOWN'),
    'RIGHT': ('UP', 'DOWN')
}



# Function untuk Score
# Score awal
score = 0

# Menampilkan score
def show_score(choice, color, font, size):
    # Score Font
    score_font = pygame.font.SysFont(font, size)

    # Render Score Surface (Text)
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # Object segi empat untuk score_surface
    score_rect = score_surface.get_rect()

    # Menampilkan text
    game_window.blit(score_surface, score_rect)

# Fungsi Game Over
def game_over():
    # Game over font
    my_font = pygame.font.SysFont('times new roman', 35)

    # Render Game over surface (Text)
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    # Object segi empat untuk game over surface object
    game_over_rect = game_over_surface.get_rect()

    # Letak text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # Menampilkan text
    game_window.blit(game_over_surface, game_over_rect)

    # Update keseluruhan display
    pygame.display.flip()

    # Check apakah menekan 'space' untuk exit
    while(True):
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                pygame.quit()
                quit()



# Function untuk menggerakan Snake
# Heuristic Function
def calculate_distance(snake_x, snake_y):
    return sqrt(pow(snake_x - fruit_position[0], 2) + pow(snake_y - fruit_position[1], 2))

# Menggerakan Snake
def move_snake():
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10


# Agar input dua tombol bersamaan tidak bertabrakan
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


# Mendapatkan gerakan selanjutnya yang tidak menghasilkan game over
def consider_direction(possible_moves):
    lowest = (sys.maxsize, '')

    for move in possible_moves:
        coor = get_next_move_coordinates(move)
        distance = calculate_distance(coor[0], coor[1])
        if distance < lowest[0] and border_check(move):
            lowest = (distance, move)

    return lowest[1]


# Check apakah ada border di depan
def border_check(move):
    if move == 'UP':
        return snake_position[1] - 10 > 0
    if move == 'DOWN':
        return snake_position[1] + 10 < window_y
    if move == 'LEFT':
        return snake_position[0] - 10 > 0
    if move == 'RIGHT':
        return snake_position[0] + 10 < window_x


# Mendapat posisi selanjutnya
def get_next_move_coordinates(move):
    if move == 'UP':
        return snake_position[0], snake_position[1] - 10
    if move == 'DOWN':
        return snake_position[0], snake_position[1] + 10
    if move == 'LEFT':
        return snake_position[0] - 10, snake_position[1]
    if move == 'RIGHT':
        return snake_position[0] + 10, snake_position[1]


# Apakah di dalam boundary atau tidak
def is_in_boundary(move, coor):
    if move == 'UP':
        return coor[1] > 0
    elif move == 'DOWN':
        return coor[1] < window_y
    elif move == 'LEFT':
        return coor[0] > 0
    else:
        return coor[0] < window_x


# Boolean untuk consider_180_deg_move
def is_move_180_deg(change_to):
    global direction

    return direction == opposite_direction[change_to]


# Mendapatkan gerakan terbaik untuk 180
def consider_180_deg_move(possible_moves, change_to):
    lowest = (sys.maxsize, '')
    possible_moves = secondary_move[change_to]  # UP, DOWN

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


# Boolean untuk check_is_eating_body
def is_eating_body(coor):
    next_move = [coor[0], coor[1]]
    if next_move in snake_body:
        return True
    return False


# Melihat apakah akan memakan body
def check_is_eating_body(possible_moves):
    global direction

    if not direction:
        game_over()

    if is_eating_body(get_next_move_coordinates(direction)):
        possible_moves.remove(direction)
        change_to = consider_direction(possible_moves)
        direction = change_to
        check_is_eating_body(possible_moves)


# Melihat gerakan terbaik untuk mendapat buah
def determine_direction(possible_moves, change_to):
    global direction

    if is_move_180_deg(change_to):
        direction = consider_180_deg_move(possible_moves, change_to)

    change_direction(change_to)
    check_is_eating_body(possible_moves)


# Main Function
while True:
    pygame.event.get() # Agar tidak error jika interaksi dengan window
    possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    # Mengganti arah selanjutnya
    change_to = consider_direction(possible_moves)

    determine_direction(possible_moves, change_to)

    move_snake()

    # Mekanisme gerakan dan penambahan body snake
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # Respawn Fruit
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    game_window.fill(black)

    # Render Snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0], pos[1], 10, 10))

    # Render Fruit
    pygame.draw.rect(game_window, purple, pygame.Rect(
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

    # Menampilkan Score
    show_score(1, white, 'times new roman', 20)

    # Refresh layar
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed)
