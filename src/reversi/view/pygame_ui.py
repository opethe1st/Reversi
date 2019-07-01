import math
from dataclasses import dataclass
from functools import wraps
from typing import Optional, Tuple

import pygame
import pygame.gfxdraw
import pygame.locals

from reversi.core import Board, Position
from reversi.core import Piece, Player

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
        self.board_dimensions = (400, 550)
        self.screen = pygame.display.set_mode(self.board_dimensions)
        self.size = 100
        self.colour_map = {
            Player.ONE: Colour.BLUE.value,
            Player.TWO: Colour.RED.value
        }

    @update_display
    def display_board(self):
        # draw the background
        pygame.draw.rect(self.screen, Colour.WHITE.value, pygame.Rect(0, 0, 400, 400), 0)

        for position, piece in self._board:
            if piece:
                draw_circle(
                    screen=self.screen,
                    size=self.size,
                    position=position,
                    colour=self.colour_map[piece.player]
                )

    @update_display
    def get_move(self, player) -> Tuple[Optional[Position], bool]:
        # block till a move is made
        # print('get-move', player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    position, is_clicked = get_clicked_ball(size=self.size)
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

    @update_display
    def display_scores(self, scores):
        print(scores)


# maybe make this is part of a pygame client and then have the UI built on top of it? But I suspect that will be too much abstraction
def draw_circle(screen, size, position: Position, colour: Colour):
    y, x = position.x + 0.5, position.y + 0.5
    pygame.gfxdraw.filled_circle(screen, int(x * size), int(y * size), size//2 - 2, colour)
    pygame.gfxdraw.aacircle(screen, int(x * size), int(y * size), size//2 - 2, colour)


def get_clicked_ball(size) -> Tuple[Optional[Position], bool]:
    x1, y1 = pygame.mouse.get_pos()
    # TODO(ope): remove constants
    for x in range(4):
        for y in range(4):
            x2, y2 = (x + 0.5) * size, (y + 0.5) * size
            distance = math.hypot(x1 - x2, y1 - y2)
            if distance <= size//2:
                return Position(y, x), True  # TODO(ope); make this clearer
    return None, False


# event stuff
# TODO(ope): Is this needed?
class Event:
    pass


@dataclass
class PositionClickedEvent(Event):
    position: Position


class GameQuit(Event):
    pass


def get_events(size):
    events = []
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            events.append(GameQuit())
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            position, is_clicked = get_clicked_ball(size=size)
            if is_clicked:
                events.append(PositionClickedEvent(position=position))
    return events


if __name__ == '__main__':
    # import sys
    while True:
        pygameUI = PygameUI(
            board=Board(
                pieces=[
                    [None, None, None, None],
                    # [Piece(Player.TWO), Piece(Player.ONE), Piece(Player.TWO), Piece(Player.TWO)],
                    # [Piece(Player.ONE), Piece(Player.ONE), Piece(Player.TWO), Piece(Player.ONE)],
                    # [Piece(Player.ONE), Piece(Player.ONE), Piece(Player.TWO), Piece(Player.ONE)],
                    # [Piece(Player.ONE), Piece(Player.ONE), Piece(Player.TWO), Piece(Player.ONE)],
                    [None, Piece(Player.ONE), Piece(Player.TWO), None],
                    [None, Piece(Player.TWO), Piece(Player.ONE), None],
                    [None, None, None, None],
                ]
            )
        )
        pygameUI.display_board()
        events = get_events(size=pygameUI.size)
        for event in events:
            if isinstance(event, GameQuit):
                pygame.quit()
            elif isinstance(event, PositionClickedEvent):
                print(event)
        pygame.display.update()
