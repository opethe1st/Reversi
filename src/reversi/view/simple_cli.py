from reversi.core import Position
from reversi.core.board import Player
from reversi.view.ui import UI


class SimpleCLI(UI):

    def __init__(self, board):
        self._board = board
        self._player_to_symbol = {
            Player.ONE: 'W',
            Player.TWO: 'B',
        }

    def get_move(self, player) -> Position:
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

    def display_game_over(self, score_counter):
        for player, score in score_counter.items():
            print(f'player: {player} scored: {score}')

    def display_skip_move(self, player):
        print(f"Skipped player: {player}'s turn since they have no valid move")

    def display_scores(self, scores):
        print(scores)

    def select_player_colour(self, player, colour):
        if player not in Player.ALL:
            print('unknown player')
        self._player_to_symbol[player] = colour
