# game_display.py

import pygame

TILE_SIZE = 20

BOARD_WIDTH = 32
BOARD_HEIGHT = 32

def draw_board(screen):
    for x in range(BOARD_WIDTH):
	    for y in range(BOARD_HEIGHT):
	        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
	        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_victory_screen(screen, on_next_level, on_exit):
    screen.fill((220, 220, 220))  # Solid background color

    font = pygame.font.Font(None, 36)
    text = font.render("Congratulations!", True, (0, 0, 0))
    screen.blit(text, (100, 50))

    button_rect = pygame.Rect(100, 120, 200, 50)  # Repositioned the "Next Level" button
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    button_text = font.render("Next Level", True, (255, 255, 255))
    screen.blit(button_text, (150, 135))

    exit_button_rect = pygame.Rect(100, 190, 200, 50)  # Repositioned the "Exit" button
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    exit_button_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_button_text, (190, 205))

    # Create button objects for "Next Level" and "Exit" buttons
    next_level_button = pygame.Rect(100, 120, 200, 50)
    exit_button = pygame.Rect(100, 190, 200, 50)

    # Attach event listeners to the buttons
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if next_level_button.collidepoint(mouse_x, mouse_y):
                on_next_level()
            elif exit_button.collidepoint(mouse_x, mouse_y):
                on_exit()

    return next_level_button, exit_button
