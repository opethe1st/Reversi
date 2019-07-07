from abc import ABC, abstractmethod
from collections import Counter

from reversi.core import Board, Player


# TODO(ope) is this useful? This just captures displaying capabilities nothing about events
# It would also be more useful, if we could make sure the concrete classes never violate this interface
#  right now, it is just checks that the names of the methods are the same
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
