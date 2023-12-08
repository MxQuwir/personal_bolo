# algorithm_tests.py

import global_vars
import unittest
from quadtree import Quadtree
from user import User
from game_object import Wall
from victory_tile import VictoryTile


id_generator = global_vars.UniqueIdGenerator()


class TestGameLevel(unittest.TestCase):



    def generate_random_level(self, quadtree):
        # Generate a random solvable game level with walls
        # You may need to implement your algorithm to create a solvable level
        # For simplicity, let's create a simple maze-like structure

        # Insert walls into the Quadtree
        for x in range(10, 91, 20):
            for y in range(10, 91, 20):
                wall = Wall(id_generator.get_unique_id(), x, y)
                quadtree.insert(wall)

    def setUp(self):
        # Initialize the game objects
        self.quadtree = Quadtree(0, 0, 100, 100)
        self.user = User(id_generator.get_unique_id(), 10, 10)
        self.victory_tile = VictoryTile(id_generator.get_unique_id(), 90, 90)

        # Insert objects into the Quadtree
        self.quadtree.insert(self.user)
        self.quadtree.insert(self.victory_tile)

        # Generate a random solvable game level
        self.generate_random_level(self.quadtree)

    def test_user_reaches_victory(self):
        # Simulate the game loop
        while not self.user.reached_victory and self.user.moves < 100:
            # Perform some game logic here, e.g., move the user based on your game rules
            # ...

            # Update the Quadtree after each move
            self.quadtree.update(self.user)

        # Check if the user reached the victory tile
        self.assertTrue(self.user.reached_victory, "User should have reached the victory tile.")
        print_game_board(self.quadtree, 100, 100)

    def test_victory(self):
        # run collision checks for user in quadtree to handle victory
        collision = self.quadtree.collides(user)
        return self.user.handle_collision(collision, self.quadtree)

    def print_game_board(quadtree, width, height):
        for y in range(height):
            for x in range(width):
                objects = quadtree.retrieve(GameObject(x, y, 1, 1))  # Replace with your object creation logic
                if any(isinstance(obj, Wall) for obj in objects):
                    print("W", end=" ")  # Wall
                elif any(isinstance(obj, User) for obj in objects):
                    print("U", end=" ")  # User
                elif any(isinstance(obj, VictoryTile) for obj in objects):
                    print("V", end=" ")  # Victory Tile
                else:
                    print(".", end=" ")  # Empty space
            print()

if __name__ == '__main__':
    unittest.main()