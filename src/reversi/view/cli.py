from typing import Tuple

from reversi.core import Position
from reversi.core.board import Player
from reversi.view.ui import UI


class CLI(UI):

    def __init__(self, board):
        self._board = board
        self._player_to_symbol = {
            Player.ONE: 'W',
            Player.TWO: 'B',
        }

    def get_move(self, player) -> Tuple[Position, bool]:
        x, y = map(int, input(f"It is player: {player}'s turn. Input a position to move to: ").split())
        return Position(x, y), True

    def display_board(self):
        def print_row(row):
            line = '|'
            for piece in row:
                if piece is None:
                    line += ' '
                else:
                    line += self._player_to_symbol[piece.player]
            line += '|'
            print(line)

        print(' ----')
        for row in self._board._pieces:  # TODO(ope): fix this break in encapsulation or not
            print_row(row)
        print(' ----')
        print()

    def display_game_over(self, scores):
        print(f'player: {Player.ONE} scored: {scores[Player.ONE]}')
        print(f'player: {Player.TWO} scored: {scores[Player.TWO]}')

    def display_skip_move(self, player):
        print(f"Skipped player: {player}'s turn since they have no valid move")

    def display_scores(self, scores):
        print(scores)
