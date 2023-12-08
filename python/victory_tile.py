# victory_tile.py


from game_object import GameObject
from image_object import ImageObject
import game_display
import random

class VictoryTile(GameObject, ImageObject):
    def __init__(self, key, x, y):
        super().__init__(key, x if x else random.randint(0, game_display.BOARD_WIDTH - 1), y if y else random.randint(0, game_display.BOARD_HEIGHT - 1))
        self.load_image("assets/victory_icon.png")

    def draw(self, screen):
	    screen.blit(self.image, (self.x * game_display.TILE_SIZE, self.y * game_display.TILE_SIZE))
