from abc import ABC, abstractmethod
from typing import Dict

from reversi.core import Board, Player

from .constants import Colour


class UI(ABC):

    @abstractmethod
    def __init__(self, board: Board):
        pass

    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def display_game_over(self):
        pass

    @abstractmethod
    def display_skip_move(self, player: Player):
        pass

    @abstractmethod
    def select_player_colour(self, player: Player, colour: Colour):
        pass

    @abstractmethod
    def display_scores(self, scores: Dict):
        pass
