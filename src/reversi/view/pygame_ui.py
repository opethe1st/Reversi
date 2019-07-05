import math
from dataclasses import dataclass
from functools import wraps
from typing import Optional, Tuple
import sys
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
# TODO(Ope): better display, say have fixed dimensions and adjust pieces to fit those dimensions
# TODO(Ope): probably write a wrapper on pygame features
class GUI(UI):

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
            Player.ONE: Colour.BLUE,
            Player.TWO: Colour.RED
        }

        self.font = pygame.font.Font('freesansbold.ttf', 32)

    @update_display
    def display_board(self):
        pygame.draw.rect(self.screen, Colour.WHITE.value, pygame.Rect(0, 0, self.board_height, self.board_width))

        for position, piece in self._board:
            if piece:
                draw_circle(
                    screen=self.screen,
                    size=self.piece_size,
                    position=position,
                    colour=self.colour_map[piece.player].value
                )

    # TODO(ope): remove type hints so it inherits from parent class
    # TODO(ope): add tests for this
    @update_display
    def get_clicked_ball(self, position: Position) -> Tuple[Optional[Position], bool]:
        x1, y1 = position.x, position.y
        width = height = self._board.size
        for x in range(width):
            for y in range(height):
                x2, y2 = (x + 0.5) * self.piece_size, (y + 0.5) * self.piece_size
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.piece_size//2:
                    return Position(y, x), True  # TODO(ope); make this clearer, why it is flipped
        return None, False # if clicked outside the board

    @update_display
    def display_game_over(self):
        text = self.font.render('Game Over', True, Colour.BLUE.value, Colour.RED.value)
        self.screen.blit(text, (450, 10))
        print('game over!')

    @update_display
    def display_skip_move(self, player):
        text = self.font.render('skipping this move', True, Colour.BLUE.value, Colour.RED.value)
        self.screen.blit(text, (450, 10))
        print('skipping this move')

    @update_display
    def select_player_colour(self, player, colour):
        self.colour_map[player] = colour

    # TODO(ope) Implement this
    @update_display
    def display_scores(self, scores):
        # can factor this into the same thing
        player_one_score = f'{self.colour_map[Player.ONE].name}: {scores[Player.ONE]}'
        player_two_score = f'{self.colour_map[Player.TWO].name}: {scores[Player.TWO]}'
        text1 = self.font.render(player_one_score, True, Colour.BLACK.value, Colour.WHITE.value)
        text2 = self.font.render(player_two_score, True, Colour.BLACK.value, Colour.WHITE.value)
        self.screen.blit(text1, (0, self.board_width), pygame.Rect(0, 0, self.score_board_height, self.score_board_height))
        self.screen.blit(text2, (0, self.board_width+75), pygame.Rect(0, 0, self.game_width, self.score_board_height))
        print(scores)



# maybe make this is part of a pygame client and then have the UI built on top of it? But I suspect that will be too much abstraction
def draw_circle(screen, size: int, position: Position, colour: Colour):
    y, x = position.x + 0.5, position.y + 0.5
    pygame.gfxdraw.filled_circle(screen, int(x * size), int(y * size), size//2 - 2, colour)
    pygame.gfxdraw.aacircle(screen, int(x * size), int(y * size), size//2 - 2, colour)
