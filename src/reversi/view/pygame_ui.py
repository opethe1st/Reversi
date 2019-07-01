import math
from dataclasses import dataclass
from functools import wraps
from typing import Optional, Tuple

import pygame  # type: ignore
import pygame.gfxdraw  # type: ignore
import pygame.locals  # type: ignore

from reversi.core import Position
from reversi.core import Player

from .ui import UI
from .constants import Colour


def update_display(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        pygame.display.update()
        return res
    return wrapper


# TODO(Ope): Remove all the magic constants
# TODO(Ope): Is it useful to make a metaclass of this so that update display is called after every method here by default + a decorator to turn if off?
class PygameUI(UI):

    def __init__(self, board):
        self._board = board
        pygame.init()
        pygame.display.set_caption('Reversi!')

        self.piece_size = 50
        self.board_width = self._board.size * self.piece_size
        self.board_height = self.board_width

        self.game_width = self.board_width
        self.score_board_height = 150
        self.game_height = board.size * self.piece_size + self.score_board_height  # need a better name than score_board_height

        self.screen = pygame.display.set_mode((self.game_width, self.game_height))

        self.colour_map = {
            Player.ONE: Colour.BLUE.value,
            Player.TWO: Colour.RED.value
        }

    @update_display
    def display_board(self):
        # draw the background
        pygame.draw.rect(self.screen, Colour.WHITE.value, pygame.Rect(0, 0, self.board_height, self.board_width))

        for position, piece in self._board:
            if piece:
                draw_circle(
                    screen=self.screen,
                    size=self.piece_size,
                    position=position,
                    colour=self.colour_map[piece.player]
                )

    # TODO(ope): remove type hints so it inherits from parent class
    @update_display
    def get_move(self, player) -> Tuple[Optional[Position], bool]:
        # block till a move is made
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    position, is_clicked = get_clicked_ball(width=self._board.size, height=self._board.size, size=self.piece_size)
                    return position, is_clicked
        return None, False  # TODO(ope); fix, it shouldn't get here

    @update_display
    def display_game_over(self):
        print('game over!')

    @update_display
    def display_skip_move(self, player):
        pass

    @update_display
    def select_player_colour(self, player, colour):
        pass

    # TODO(ope) Implement this
    @update_display
    def display_scores(self, scores):
        print(scores)


# maybe make this is part of a pygame client and then have the UI built on top of it? But I suspect that will be too much abstraction
def draw_circle(screen, size: int, position: Position, colour: Colour):
    y, x = position.x + 0.5, position.y + 0.5
    pygame.gfxdraw.filled_circle(screen, int(x * size), int(y * size), size//2 - 2, colour)
    pygame.gfxdraw.aacircle(screen, int(x * size), int(y * size), size//2 - 2, colour)


def get_clicked_ball(width, height, size: int) -> Tuple[Optional[Position], bool]:
    x1, y1 = pygame.mouse.get_pos()
    # TODO(ope): remove constants
    for x in range(width):
        for y in range(height):
            x2, y2 = (x + 0.5) * size, (y + 0.5) * size
            distance = math.hypot(x1 - x2, y1 - y2)
            if distance <= size//2:
                return Position(y, x), True  # TODO(ope); make this clearer
    return None, False
