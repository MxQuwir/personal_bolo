import unittest
from quadtree import Quadtree
from game_object import GameObject

class TestQuadtree(unittest.TestCase):
    def setUp(self):
        # Initialize a quadtree with a specific area
        self.quadtree = Quadtree(0, 0, 100, 100)

    def test_insert_and_retrieve(self):
        # Create a test object
        test_object = GameObject(50, 50)

        # Insert the object into the quadtree
        self.quadtree.insert(test_object)

        # Retrieve objects from the quadtree
        retrieved_objects = self.quadtree.retrieve(test_object)

        # Ensure that the test object is in the retrieved objects list
        self.assertIn(test_object, retrieved_objects)

    def test_subdivide(self):
        # Subdivide the quadtree
        self.quadtree.subdivide()

        # Ensure that the quadtree now has child nodes
        self.assertIsNotNone(self.quadtree.nodes[0])

    def test_contains(self):
        # Create a test object
        test_object = GameObject(50, 50)

        # Check if the quadtree contains the test object
        self.assertTrue(self.quadtree.contains(test_object))

        # Check if a point outside the quadtree is not contained
        self.assertFalse(self.quadtree.contains(GameObject(200, 200)))

    def test_update(self):
        # Create a test object
        test_object = GameObject(50, 50)

        # Insert the object into the quadtree
        self.quadtree.insert(test_object)

        # Update the position of the object
        test_object.x = 60
        test_object.y = 60

        # Update the quadtree to reflect the object's new position
        self.quadtree.update(test_object)

        # Retrieve objects from the quadtree
        retrieved_objects = self.quadtree.retrieve(test_object)

        # Ensure that the test object is in the retrieved objects list
        self.assertIn(test_object, retrieved_objects)

    def test_insert_after_subdivide(self):
        # Create a quadtree with max_objects set to 2
        quadtree = Quadtree(0, 0, 100, 100, max_objects=2)
        
        # Insert two objects, causing the quadtree to subdivide
        quadtree.insert(GameObject(10, 10))
        quadtree.insert(GameObject(20, 20))
        
        # Attempt to insert a third object
        quadtree.insert(GameObject(30, 30))
        
        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node
        
        
        quadtree.insert(GameObject(3, 30))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(5, 30))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(7, 30))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(3, 3))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(3, 7))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(3, 22))
        assert len(quadtree.objects) == 0 


        quadtree.insert(GameObject(12, 15))
        assert len(quadtree.objects) == 0 

    def test_update_after_subdivide(self):
        quadtree = Quadtree(0, 0, 100, 100)
        
        # Insert two objects, causing the quadtree to subdivide
        quadtree.insert(GameObject(10, 10))
        quadtree.insert(GameObject(20, 20))
        
        # Attempt to insert a third object
        game_object = GameObject(30, 30)
        quadtree.insert(game_object)


        quadtree.insert(GameObject(11, 11))
        quadtree.insert(GameObject(22, 22))
        
        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node

        quadtree.update(game_object)

        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node

        quadtree.update(game_object)
        
        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node

        quadtree.update(game_object)
        
        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node

        quadtree.update(game_object)
        
        # Check if the third object is in the quadtree
        assert len(quadtree.objects) == 0  # Since it should have been moved to a child node

if __name__ == '__main__':
    unittest.main()