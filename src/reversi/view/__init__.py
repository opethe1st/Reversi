from abc import ABC, abstractmethod


class UI(ABC):

    @abstractmethod
    def get_move(self, player):
        pass

    @abstractmethod
    def display_board(self, board, score_counter):
        pass

    @abstractmethod
    def display_game_over(self, score_counter):
        pass

    @abstractmethod
    def display_skip_move(self, player):
        pass

    @abstractmethod
    def select_player_colour(self, player, colour):
        pass
