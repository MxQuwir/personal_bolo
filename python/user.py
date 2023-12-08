# user.py

from game_object import GameObject, Wall
from image_object import ImageObject
import game_display
from quadtree import Quadtree

from victory_tile import VictoryTile
from box import Box

class User(GameObject, ImageObject):
    def __init__(self, key, x, y):
        super().__init__(key, x, y)
        self.load_image("assets/user_icon.png")  # Load the user icon image

    def attempt_update(self, dx, dy):
        self.xAttempt = max(0, min(game_display.BOARD_WIDTH - 1, self.x + dx))
        self.yAttempt = max(0, min(game_display.BOARD_HEIGHT - 1, self.y + dy))

    def update_position(self, dx, dy):
        # Update the user's position by dx and dy
        self.x = max(0, min(game_display.BOARD_WIDTH - 1, self.x + dx))
        self.y = max(0, min(game_display.BOARD_HEIGHT - 1, self.y + dy))

    def draw(self, screen):
        screen.blit(self.image, (self.x * game_display.TILE_SIZE, self.y * game_display.TILE_SIZE))

    def handle_collision(self, obj, quadtree):
        print("handle user collision")
        if isinstance(obj, Wall):
            self.cancel_attempt()
            return False
        elif isinstance(obj, VictoryTile):
            self.accept_attempt()
            #only True for victory!
            return True
        elif isinstance(obj, Box):
            obj.xAttempt = obj.x + self.xAttempt - self.x
            obj.yAttempt = obj.y + self.yAttempt - self.y
            collision = quadtree.collides(obj)
            can_move = True
            if collision:
                can_move = obj.handle_collision(collision, quadtree)

            if (obj.xAttempt > (game_display.BOARD_WIDTH - 1) 
            or obj.yAttempt > (game_display.BOARD_HEIGHT - 1)
            or obj.xAttempt < 0 or obj.yAttempt < 0):
                can_move = False

            if can_move:
                obj.accept_attempt()
                self.accept_attempt()
                quadtree.update(self)
                quadtree.update(obj)
            else:
                self.cancel_attempt
                obj.cancel_attempt

            return False
                


        