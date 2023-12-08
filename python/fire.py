# fire.py

from game_object import GameObject
import pygame
import game_display

class Box(GameObject, ImageObject):
	def __init__(self, key, x, y):
		super().__init__(key, x, y)
		self.load_image("assets/fire.png")

    def draw(self, screen):
	    screen.blit(self.image, (self.x * game_display.TILE_SIZE, self.y * game_display.TILE_SIZE))

	