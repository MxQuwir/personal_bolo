import logging

# Import the logger from the main script
logger = logging.getLogger(__name__)

class Quadtree:
    def __init__(self, x, y, width, height, max_objects=4, max_depth=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_objects = max_objects
        self.max_depth = max_depth

        self.objects = []
        self.nodes = [None, None, None, None]

    def __contains__(self, obj):
        return obj.key in [o.key for o in self.objects]

    def __str__(self):
        ret_string = ""
        for obj in self.objects:
            ret_string += str(obj)
    
        if self.nodes[0] is not None:
            ret_string += "parent::"
            for node in self.nodes:
                ret_string += "node:" + str(node)

        return ret_string

    def remove_object_by_id(self, key):
        self.objects = [obj for obj in self.objects if obj.key != key]

    def insert(self, obj):
        logger.debug(f"insert {str(obj)} into {str(self)}")
        if len(self.objects) < self.max_objects and self.nodes[0] is None:
            logger.debug(f"appending to current")
            self.objects.append(obj)
        else:
            if self.nodes[0] is None:
                self.subdivide()

            for node in self.nodes:
                if node.contains(obj):
                    node.insert(obj)

        logger.debug(f"insert end {str(self)}")

    def subdivide(self):
        logger.debug("subdivide")
        sub_width = self.width // 2
        sub_height = self.height // 2
        x, y = self.x, self.y

        self.nodes[0] = Quadtree(x + sub_width, y, sub_width, sub_height)
        self.nodes[1] = Quadtree(x, y, sub_width, sub_height)
        self.nodes[2] = Quadtree(x, y + sub_height, sub_width, sub_height)
        self.nodes[3] = Quadtree(x + sub_width, y + sub_height, sub_width, sub_height)

        # Reinsert objects into child nodes
        for obj in self.objects:
            for node in self.nodes:
                if node.contains(obj):
                    node.insert(obj)

        # Clear objects in parent node
        self.objects = []

    def contains(self, obj):
        logger.debug(f"contains: {self.x}|{obj.x}|{self.x+self.width},{self.y}|{self.y}|{self.y+self.height} x,y self.low|obj|self.high ")
        return (
            self.x <= obj.x < self.x + self.width and
            self.y <= obj.y < self.y + self.height
        )

    def contains_attempt(self, obj):
        logger.debug(f"contains_attempt: {self.x}|{obj.x}|{self.x+self.width},{self.y}|{self.y}|{self.y+self.height} x,y self.low|obj|self.high ")
        return (
            self.x <= obj.xAttempt < self.x + self.width and
            self.y <= obj.yAttempt < self.y + self.height
        )

    def retrieve(self, obj):
        logger.debug(f"retrieve {str(obj)}")
        objects = self.objects

        if self.nodes[0] is not None:
            for node in self.nodes:
                if node.contains(obj):
                    objects.extend(node.retrieve(obj))


        logger.debug(f"retrieve found {str(objects)}")
        return objects

    def remove_object(self, obj):
        logger.debug(f"remove_object {str(obj)}")
        if obj in self.objects:
            logger.debug(f"before remove {str(self)}")
            self.remove_object_by_id(obj.key)
            logger.debug(f"after remove {str(self)}")
            return True
        elif self.nodes[0] is not None:
            for node in self.nodes:
                if node.remove_object(obj):
                    return True
        return False

    def update(self, obj):
        logger.debug(f"update {str(obj)}")
        if not self.remove_object(obj):
            logger.error("Object unexpectedly not found: %s", str(obj))

        self.insert(obj)

    def retreive_possible_collisions(self, obj):
        logger.debug(f"retreive_possible_collisions")
        if self.nodes[0] is not None:
            for node in self.nodes:
                if node.contains_attempt(obj):
                    return node.retreive_possible_collisions(obj)

        else:
            return self.objects


    def collides(self, obj):
        logger.debug(f"collides obj {str(obj)} self {str(self)}")
        possible_collisions = self.retreive_possible_collisions(obj)

        if possible_collisions is not None and len(possible_collisions) > 0 and possible_collisions[0] is not None:
            for collidable in possible_collisions:
                if obj.xAttempt == collidable.x and obj.yAttempt == collidable.y and obj != collidable:
                    return collidable

        return False
