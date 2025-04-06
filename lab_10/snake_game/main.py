
import sys
from pathlib import Path
import pygame

import config
from game.snake import Snake
from game.fruit import Fruit
from game.state import GameState
from input.handler import get_commands, Command
from ui.renderer import Renderer

SAVE_FILE = Path("savegame.json")


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Create game objects
    snake = Snake()
    fruit = Fruit(config.CELL_NUMBER)
    renderer = Renderer(screen, config, font)

    paused = False
    score = 0

    # Main game loop
    while True:
        cmds = get_commands()

        # Handle quit
        if Command.QUIT in cmds:
            pygame.quit()
            sys.exit()

        # Toggle pause
        if Command.PAUSE in cmds:
            paused = not paused

        if Command.SAVE in cmds:
            state = GameState(snake, fruit, score)
            state.save(SAVE_FILE)

        # Load game
        if Command.LOAD in cmds and SAVE_FILE.exists():
            state = GameState.load(SAVE_FILE, snake, fruit)
            score = state.score
            paused = False

        if not paused:
            for cmd in cmds:
                if cmd in (Command.UP, Command.DOWN, Command.LEFT, Command.RIGHT):
                    snake.set_direction(cmd.name)

            snake.move()

            # Check eating
            if snake.check_eat(fruit):
                snake.grow()
                score += 1
                fruit.randomize()

            # Check collisions
            if snake.check_self_collision() or snake.check_wall_collision(config.CELL_NUMBER, config.CELL_NUMBER):
                snake.reset()
                score = 0

        renderer.render(snake, fruit, score, paused)

        clock.tick(config.FPS)


if __name__ == "__main__":
    main()