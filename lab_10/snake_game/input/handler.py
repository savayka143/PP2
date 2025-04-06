
from enum import Enum, auto
import pygame

class Command(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()
    PAUSE = auto()
    SAVE  = auto()
    LOAD  = auto()
    QUIT  = auto()


def get_commands():
    cmds = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cmds.append(Command.QUIT)

        elif event.type == pygame.KEYDOWN:
            mapping = {
                pygame.K_UP:    Command.UP,
                pygame.K_DOWN:  Command.DOWN,
                pygame.K_LEFT:  Command.LEFT,
                pygame.K_RIGHT: Command.RIGHT,
                pygame.K_p:     Command.PAUSE,
                pygame.K_s:     Command.SAVE,
                pygame.K_l:     Command.LOAD,
            }
            cmd = mapping.get(event.key)
            if cmd:
                cmds.append(cmd)

    return cmds