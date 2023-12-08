# game_object.py

import pygame
import game_display


class GameObject:
    def __init__(self, key, x, y):
        self._key = key 
        self._x = x
        self._y = y
        self._xAttempt = x
        self._yAttempt = y

    def __str__(self):
        return f"[key={self.key}, x={self.x}, y={self.y}]"
    
    @property
    def key(self):
        return self._key

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def xAttempt(self):
        return self._xAttempt

    @property
    def yAttempt(self):
        return self._yAttempt

    @xAttempt.setter
    def xAttempt(self, value):
        self._xAttempt = value

    @yAttempt.setter
    def yAttempt(self, value):
        self._yAttempt = value

    def handle_collision(self, obj, quadtree):
        # Default collision behavior (to be overridden in subclasses)
        pass

    def draw(self, screen):
        # Default draw behavior (to be overridden in subclasses)
        pass

    def accept_attempt(self):
        self.x = self.xAttempt
        self.y = self.yAttempt
    
    def cancel_attempt(self):
        self.xAttempt = self.x
        self.yAttempt = self.y

    def equals(self, obj):
        return self.key == obj.key

class Wall(GameObject):
    def __init__(self, key, x, y):
        super().__init__(key, x, y)


    def draw(self, screen):
        # Load the wall image
        self.image = pygame.Surface((game_display.TILE_SIZE, game_display.TILE_SIZE))
        self.image.fill((255, 0, 0))  # Fill with a red color
        screen.blit(self.image, (self.x * game_display.TILE_SIZE, self.y * game_display.TILE_SIZE))

    