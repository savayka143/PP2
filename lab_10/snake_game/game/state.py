# game/state.py

import json
from pathlib import Path
from pygame.math import Vector2

class GameState:
    def __init__(self, snake, fruit, score, level=1):
        # Convert every Vector2 into a plain [x, y] list of ints
        self.snake_body = [[int(b.x), int(b.y)] for b in snake.body]
        self.snake_dir  = [int(snake.direction.x), int(snake.direction.y)]
        self.fruit_pos  = [int(fruit.pos.x), int(fruit.pos.y)]
        self.score      = score
        self.level      = level

    def to_dict(self):
        return {
            "snake_body": self.snake_body,
            "snake_dir" : self.snake_dir,
            "fruit_pos" : self.fruit_pos,
            "score"     : self.score,
            "level"     : self.level
        }

    @classmethod
    def from_dict(cls, data, snake, fruit):
        # Reconstruct the Vector2 objects from the lists
        snake.body = [Vector2(x, y) for x, y in data["snake_body"]]
        snake.direction = Vector2(*data["snake_dir"])
        fruit.pos = Vector2(*data["fruit_pos"])
        score = data["score"]
        level = data.get("level", 1)
        return cls(snake, fruit, score, level)

    def save(self, path: Path):
        # This will now only contain ints and lists
        with path.open("w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def load(path: Path, snake, fruit):
        with path.open() as f:
            data = json.load(f)
        return GameState.from_dict(data, snake, fruit)
