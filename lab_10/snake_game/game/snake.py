
from pygame.math import Vector2

class Snake:
    def __init__(self, start_positions=None):
        self.body = start_positions or [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.growing = False

    def set_direction(self, command):
        if command == 'UP' and self.direction.y != 1:
            self.direction = Vector2(0, -1)
        elif command == 'DOWN' and self.direction.y != -1:
            self.direction = Vector2(0, 1)
        elif command == 'LEFT' and self.direction.x != 1:
            self.direction = Vector2(-1, 0)
        elif command == 'RIGHT' and self.direction.x != -1:
            self.direction = Vector2(1, 0)

    def move(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def reset(self, start_positions=None):
        self.body = start_positions or [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.growing = False

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def check_wall_collision(self, grid_width, grid_height):
        head = self.body[0]
        return not (0 <= head.x < grid_width and 0 <= head.y < grid_height)

    def check_eat(self, fruit):
        return self.body[0] == fruit.pos