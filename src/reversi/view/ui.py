from abc import ABC, abstractmethod
from collections import Counter

from reversi.core import Board, Player


# is this workable? - having this interface?
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
    def display_score_board(self, scores: Counter, player_to_play: Player):
        pass
