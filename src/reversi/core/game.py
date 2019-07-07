from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set, Tuple

from .board import Board, Piece
from .player import Player
from .position import (
    CardinalDirection,
    Direction,
    Position,
    next_position_in_direction
)


class Game:
    '''This class contains game rules'''

    def __init__(self, board: Board):
        # for now, all boards start the same
        self._board = board

    def is_over(self):
        return all(not(self.compute_valid_moves(player=player)) for player in Player)

    def compute_scores(self) -> Counter:
        return Counter([piece.player for _, piece in self._board if piece])  # type: ignore

    def play_move(self, position: Position, player: Player) -> bool:
        # This violates CQRS?
        '''modifies board and returns True if this is a valid move'''
        moves = self.compute_valid_moves(player=player)
        if position not in moves:
            return False
        for origin, direction in moves[position]:
            _capture_pieces(start=origin, end=position, direction=direction, player=player, board=self._board)
        return True

    def compute_valid_moves(self, player: Player) -> Dict[Position, List[Tuple[Position, Direction]]]:
        positions = _get_positions_with_player_piece(board=self._board, player=player)
        moves: Dict[Position, List] = defaultdict(list)
        for position in positions:
            for direction in CardinalDirection:
                valid_position, is_valid = _compute_valid_move(
                    position=position,
                    direction=direction.value,
                    board=self._board,
                    player=player
                )
                if is_valid:
                    moves[valid_position].append((position, direction.value))  # type: ignore
        return moves


# some utility functions
def _get_positions_with_player_piece(board: Board, player: Player) -> Set[Position]:
    return {position for position, piece in board if piece and piece.player == player}  # type: ignore


def _compute_valid_move(board: Board, position: Position, direction: Direction, player: Player) -> Tuple[Optional[Position], bool]:
    '''return a valid position to move to, or False if there is None'''
    other_player_seen = False
    current_position = position
    # woah, just found out about this! you can efficiently check ranges with 4 in range(123)!
    while (current_position.x in range(board.size)) and (current_position.y in range(board.size)):
        current_piece = board.get_piece_at_position(position=current_position)
        if other_player_seen and current_piece is None:
            return current_position, True
        elif current_piece is not None and current_piece.player != player:
            other_player_seen = True
        current_position = next_position_in_direction(position=current_position, direction=direction)
    return None, False


def _capture_pieces(board: Board, start: Position, end: Position, direction: Direction, player: Player):
    position = start
    while position != end:
        board.set_piece_at_position(position=position, piece=Piece(player=player))
        position = next_position_in_direction(position=position, direction=direction)
    # set piece at the end too.
    board.set_piece_at_position(position=position, piece=Piece(player=player))
