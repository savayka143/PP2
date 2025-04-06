import random
from pygame.math import Vector2

class Fruit:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.pos = Vector2(0, 0)
        self.randomize()

    def randomize(self):
        x = random.randint(0, self.grid_size - 1)
        y = random.randint(0, self.grid_size - 1)
        self.pos = Vector2(x, y)