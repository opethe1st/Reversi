from abc import ABC, abstractmethod


class UI(ABC):

    @abstractmethod
    def get_move(self, player):
        pass

    @abstractmethod
    def display_board(self, board):
        pass

    @abstractmethod
    def display_score(self, score_counter):
        pass

    @abstractmethod
    def display_skip_move(player):
        pass
