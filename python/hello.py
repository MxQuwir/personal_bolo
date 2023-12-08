import pygame
import sys
import random

# Constants
BOARD_WIDTH = 30
BOARD_HEIGHT = 25
TILE_SIZE = 20
USER_COLOR = (255, 0, 0)
VICTORY_COLOR = (0, 255, 0)
FPS = 60

# Initialize Pygame
pygame.init()

# Create the display
WINDOW_SIZE = (BOARD_WIDTH * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Simple Game")

# Load user icon image
user_icon = pygame.image.load("user_icon.png")
user_icon = pygame.transform.scale(user_icon, (TILE_SIZE, TILE_SIZE))

# Load victory icon image
victory_icon = pygame.image.load("victory_icon.png")
victory_icon = pygame.transform.scale(victory_icon, (TILE_SIZE, TILE_SIZE))

# Initial user position
user_x, user_y = 0, 0

# Randomly set victory tile position
victory_tile_x, victory_tile_y = random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1)

# Victory screen flag
victory_screen_active = False

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_board():
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_user_icon():
    screen.blit(user_icon, (user_x * TILE_SIZE, user_y * TILE_SIZE))

def draw_victory_tile():
    screen.blit(victory_icon, (victory_tile_x * TILE_SIZE, victory_tile_y * TILE_SIZE))

def draw_victory_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Congratulations!", True, (0, 0, 0))
    screen.blit(text, (80, 150))

    button_rect = pygame.Rect(100, 200, 200, 50)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    button_text = font.render("Next Level", True, (255, 255, 255))
    screen.blit(button_text, (150, 215))

    exit_button_rect = pygame.Rect(100, 280, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    exit_button_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_button_text, (190, 295))

def check_victory():
    return user_x == victory_tile_x and user_y == victory_tile_y

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and user_x > 0:
                user_x -= 1
            elif event.key == pygame.K_RIGHT and user_x < BOARD_WIDTH - 1:
                user_x += 1
            elif event.key == pygame.K_UP and user_y > 0:
                user_y -= 1
            elif event.key == pygame.K_DOWN and user_y < BOARD_HEIGHT - 1:
                user_y += 1

    # Check victory condition
    if check_victory():
        victory_screen_active = True

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw game elements
    draw_board()
    draw_user_icon()
    draw_victory_tile()

    # Draw victory screen if active
    if victory_screen_active:
        draw_victory_screen()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        # Check if the "Next Level" button is clicked
        if 100 < mouse_x < 300 and 200 < mouse_y < 250 and click:
            # Reset the victory tile position to a new random location
            victory_tile_x, victory_tile_y = random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1)
            victory_screen_active = False

        # Check if the "Exit" button is clicked
        elif 100 < mouse_x < 300 and 280 < mouse_y < 330 and click:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.update()

    # Control frame rate
    clock.tick(FPS)
