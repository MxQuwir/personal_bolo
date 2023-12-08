# main.py

import pygame
import sys
import game_display
import global_vars

from user import User
from victory_tile import VictoryTile
from game_object import Wall
from box import Box
from quadtree import Quadtree

import argparse
import logging


#Read args and set logging
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Constants
FPS = 60

# Initialize Pygame
pygame.init()

# Create the display
WINDOW_SIZE = (game_display.BOARD_WIDTH * game_display.TILE_SIZE, game_display.BOARD_HEIGHT * game_display.TILE_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Simple Game")

# Create the quadtree
quadtree = Quadtree(0, 0, game_display.BOARD_WIDTH, game_display.BOARD_HEIGHT)

id_generator = global_vars.UniqueIdGenerator()

# Create the user object
user = User(id_generator.get_unique_id(), 0, 0)

# Create the victory object
victory = VictoryTile(id_generator.get_unique_id())

box = Box(id_generator.get_unique_id(),3,3)

# Create a wall
wall_12_12 = Wall(id_generator.get_unique_id(),12,12)
wall_13_13 = Wall(id_generator.get_unique_id(),13,13)

walls = []

walls.append(wall_12_12)
walls.append(wall_13_13)

# Add the user and victory objects to the quadtree
quadtree.insert(user)
quadtree.insert(victory)
quadtree.insert(box)
quadtree.insert(wall_12_12)
quadtree.insert(wall_13_13)


# Victory screen flag
victory_screen_active = False

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define functions for button actions
def on_next_level():
    global victory_screen_active, user, victory, quadtree
    victory_screen_active = False  # Hide the victory screen
    reset_player_position()  # Restart the current level (reset user position)
    quadtree.update(user)
    # using update will work for victory once a more managed 
    # comparison system is used
    quadtree.remove_object(victory)

    victory = VictoryTile(victory.key)  # Generate a new victory tile
    
    quadtree.insert(victory)

def on_exit():
    pygame.quit()
    sys.exit()

def reset_player_position():
    global user
    user.x = 0
    user.y = 0
    user.xAttempt = 0
    user.yAttempt = 0

# Constants
MOVE_EVENT = pygame.USEREVENT + 1
MOVE_DELAY = 200  # Time delay between each move in milliseconds

# Main game loop
last_move_time = 0  # Initialize last_move_time before the loop starts
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Set the custom move event timer when an arrow key is pressed
        if not victory_screen_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                user.attempt_update(0, -1)
                last_move_time=pygame.time.get_ticks()
                pygame.time.set_timer(MOVE_EVENT, MOVE_DELAY)
            elif event.key == pygame.K_DOWN:
                user.attempt_update(0, 1)
                last_move_time=pygame.time.get_ticks()
                pygame.time.set_timer(MOVE_EVENT, MOVE_DELAY)
            elif event.key == pygame.K_LEFT:
                user.attempt_update(-1, 0)
                last_move_time=pygame.time.get_ticks()
                pygame.time.set_timer(MOVE_EVENT, MOVE_DELAY)
            elif event.key == pygame.K_RIGHT:
                user.attempt_update(1, 0)
                last_move_time=pygame.time.get_ticks()
                pygame.time.set_timer(MOVE_EVENT, MOVE_DELAY)

        # Clear the move event timer when an arrow key is released
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                pygame.time.set_timer(MOVE_EVENT, 0)

    # Move the user icon when the custom move event is triggered
    ticks=pygame.time.get_ticks()
    if ticks - last_move_time >= MOVE_DELAY:
        last_move_time = ticks

        if not victory_screen_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                user.attempt_update(0, -1)
            if keys[pygame.K_DOWN]:
                user.attempt_update(0, 1)
            if keys[pygame.K_LEFT]:
                user.attempt_update(-1, 0)
            if keys[pygame.K_RIGHT]:
                user.attempt_update(1, 0)

    if user.xAttempt != user.x or user.yAttempt != user.y:
        collision = quadtree.collides(user)

        print(str(quadtree))        
        print(collision)
        if collision:
            victory_screen_active = user.handle_collision(collision, quadtree)
        else:
            user.accept_attempt()    
            quadtree.update(user)

    # Update the game display
    screen.fill((255, 255, 255))  # Clear the screen with a white background
    game_display.draw_board(screen)
    user.draw(screen)
    victory.draw(screen)
    box.draw(screen)
    for wall in walls:
        wall.draw(screen)

    if victory_screen_active:
        # Draw the victory screen with event listeners attached
        next_level_button, exit_button = game_display.draw_victory_screen(screen, on_next_level, on_exit)

    pygame.display.flip()
    clock.tick(FPS)
    