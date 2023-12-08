# box.py

from game_object import GameObject, Wall
import pygame
import game_display

from victory_tile import VictoryTile

class Box(GameObject):
	def __init__(self, key, x, y):
		super().__init__(key, x, y)


	def draw(self, screen):
    	# Load the wall image
		self.image = pygame.Surface((game_display.TILE_SIZE, game_display.TILE_SIZE))
		self.image.fill((0, 255, 0))  # Fill with a green color
		screen.blit(self.image, (self.x * game_display.TILE_SIZE, self.y * game_display.TILE_SIZE))

	def handle_collision(self, obj, quadree):
		if isinstance(obj, Wall):
			self.cancel_attempt()
			return False
		elif isinstance(obj, VictoryTile):
			self.cancel_attempt()
			return False