# image_object.py

import pygame
import game_display

class ImageObject:
    def load_image(self, image_path):
        # Load the image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (game_display.TILE_SIZE, game_display.TILE_SIZE))