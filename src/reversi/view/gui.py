import math
from functools import wraps

import pygame  # type: ignore
import pygame.gfxdraw  # type: ignore
import pygame.locals  # type: ignore

from reversi.core import Player, Position

from .constants import Colour
from .ui import UI


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

        self.font = pygame.font.Font('freesansbold.ttf', 16)

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

    # TODO(ope): add tests for this
    @update_display
    def get_clicked_ball(self, position):
        x1, y1 = position.x, position.y
        width = height = self._board.size
        for x in range(width):
            for y in range(height):
                x2, y2 = (x + 0.5) * self.piece_size, (y + 0.5) * self.piece_size
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.piece_size//2:
                    return Position(x, y), True
        return None, False  # if clicked outside the board, return None

    @update_display
    def display_game_over(self, scores):
        if scores[Player.ONE] == scores[Player.TWO]:
            game_over_text = f"GAME OVER! Its a draw!"
        else:
            winner = Player.ONE if scores[Player.ONE] > scores[Player.TWO] else Player.TWO
            game_over_text = f"GAME OVER! {self.colour_map[winner].name} won!"

        pygame.draw.rect(self.screen, Colour.GREY.value, pygame.Rect(0, self.board_height, self.board_width, self.score_board_height))

        game_over = self.font.render(
            game_over_text,
            True,
            Colour.BLACK.value,
            Colour.GREY.value
        ).convert()
        game_over_rect = game_over.get_rect()
        self.screen.blit(
            game_over,
            (self.board_width//2 - game_over_rect.width//2, self.board_height+game_over_rect.height+self.score_board_height//4),
        )

    # TODO(ope): I am not sure this works, need to test
    @update_display
    def display_skip_move(self, skipped_player, player_to_play):
        pygame.draw.rect(self.screen, Colour.GREY.value, pygame.Rect(0, self.board_height, self.board_width, self.score_board_height))
        players_turn = self.font.render(
            f"It is {self.colour_map[player_to_play].name}'s turn again because {self.colour_map[skipped_player].name} has no valid moves",
            True,
            Colour.BLACK.value,
            Colour.GREY.value
        ).convert()
        players_turn_rect = players_turn.get_rect()
        self.screen.blit(
            players_turn,
            (self.board_width//2 - players_turn_rect.width//2, self.board_height+self.score_board_height//6),
        )

    @update_display
    def display_score_board(self, scores, player_to_play):
        # TODO(ope): this is very low level code, I probably need a layer on top of pygame
        pygame.draw.rect(self.screen, Colour.GREY.value, pygame.Rect(0, self.board_height, self.board_width, self.score_board_height))

        players_turn = self.font.render(
            f"It is {self.colour_map[player_to_play].name}'s turn",
            True,
            Colour.BLACK.value,
            Colour.GREY.value
        ).convert()
        players_turn_rect = players_turn.get_rect()
        self.screen.blit(
            players_turn,
            (self.board_width//2 - players_turn_rect.width//2, self.board_height+self.score_board_height//6),
        )

        player_one_score = f'{self.colour_map[Player.ONE].name}: {scores[Player.ONE]}'
        player_two_score = f'{self.colour_map[Player.TWO].name}: {scores[Player.TWO]}'
        score = self.font.render(
            f'{player_one_score}    {player_two_score}',
            True,
            Colour.BLACK.value,
            Colour.GREY.value
        ).convert()
        rect = score.get_rect()

        # center this
        self.screen.blit(
            score,
            (self.board_width//2 - rect.width//2, self.board_height+players_turn_rect.height+self.score_board_height//3),
        )


# maybe make this is part of a pygame client and then have the UI built on top of it? But I suspect that will be too much abstraction
def draw_circle(screen, size: int, position: Position, colour: Colour):
    y, x = position.x + 0.5, position.y + 0.5
    pygame.gfxdraw.filled_circle(screen, int(x * size), int(y * size), size//2 - 2, colour)
    pygame.gfxdraw.aacircle(screen, int(x * size), int(y * size), size//2 - 2, colour)
