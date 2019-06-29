from collections import Counter, defaultdict
from itertools import cycle
from typing import Dict, List, Tuple

from reversi.view import UI

from .board import Board, Piece, Player
from .position import CardinalDirection, Position
from .utils import (
    _capture_pieces,
    _compute_valid_move,
    _get_positions_with_player_piece
)


class Game:

    def __init__(self):
        # for now, all boards start the same
        self._board = Board(
            [
                [None, None, None, None],
                [None, Piece(Player.WHITE), Piece(Player.BLACK), None],
                [None, Piece(Player.BLACK), Piece(Player.WHITE), None],
                [None, None, None, None],
            ]
        )

    # possibly move this out
    def play_game(self, ui: UI):
        players = [Player.BLACK, Player.WHITE]
        for player in cycle(players):
            if self.is_game_over():
                score_counter = self.compute_score()
                ui.display_score({player: score_counter.get(player, 0) for player in players})
                break

            ui.display_board(self._board)
            if self.compute_valid_moves(player=player): # need to address this mismatch between player and player
                x, y = ui.get_move(player)
                #  should also check if there is a invalid move and prompt player to retry or hint on what the valid moves are.
                self.play_move(position=Position(x, y), player=player)
            else:
                ui.display_skip_move(player=player)

    # all of this should probably be private
    def is_game_over(self):
        return all(not(self.compute_valid_moves(player=player)) for player in Player.ALL)

    def compute_score(self) -> int:
        return Counter([piece.player for _, piece in self._board if piece])

    def play_move(self, position: Position, player: Player) -> bool:
        # This violates CQRS?
        '''modifies board and returns True if this is a valid move'''
        moves = self.compute_valid_moves(player=player)
        if position not in moves:
            return False
        for origin, direction in moves[position]:
            _capture_pieces(start=origin, end=position, direction=direction, player=player, board=self._board)
        return True

    def compute_valid_moves(self, player: Player) -> Dict[Position, List[Tuple[Position, CardinalDirection]]]:
        positions = _get_positions_with_player_piece(board=self._board, player=player)
        moves = defaultdict(list)
        for position in positions:
            for direction in CardinalDirection.ALL:
                valid_position = _compute_valid_move(
                    position=position,
                    direction=direction,
                    board=self._board,
                    player=player
                )
                if valid_position:
                    moves[valid_position].append((position, direction))
        return moves
