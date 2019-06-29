from typing import Tuple

from reversi.core.board import Player
from reversi.view import UI


class SimpleCLI(UI):

    def get_move(self, player) -> Tuple[int, int]:
        return map(int, input(f"It is player: {player}'s turn. Input a position to move to: ").split())

    def display_board(self, board):
        def print_row(row):
            line = '|'
            player_to_symbol = {
                Player.WHITE: 'W',
                Player.BLACK: 'B',
            }
            for piece in row:
                if piece is None:
                    line += ' '
                else:
                    line += player_to_symbol[piece.player]
            line += '|'
            print(line)

        print(' ----')
        for row in board._pieces:
            print_row(row)
        print(' ----')
        print()

    def display_score(self, score_counter):
        for player, score in score_counter.items():
            print(f'player: {player} scored: {score}')

    def display_skip_move(self, player):
        print(f"Skipped player: {player}'s turn since they have no valid move")
