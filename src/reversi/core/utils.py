from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Union

from .board import Board, Player, Piece
from .position import CardinalDirection, Position


# I like to move utils out because if not the class becomes bloated

def _get_positions_with_player_piece(board: Board, player: Player) -> Set[Position]:
    return {position for position, piece in board if piece and piece.player == player}


def _compute_valid_move(position: Position, direction: CardinalDirection, board: Board, player: Player) -> Union["False", Position]:
    other_player_seen = False
    current_position = position
    valid_moves = set()
    # woah, just found out about this! you can efficiently check ranges with 4 in range(123)!
    while (current_position.x in range(board.size)) and (current_position.y in range(board.size)):
        current_piece = board.get_piece_at_position(position=current_position)
        if other_player_seen and current_piece is None:
            return current_position
        elif current_piece is not None and current_piece.player != player:
            other_player_seen = True
        current_position = Position(x=current_position.x+direction.dx, y=current_position.y+direction.dy)
    return False


def _capture_pieces(start: int, end: int, direction: CardinalDirection, player: Player, board: Board):
    position = start
    while position != end:
        board.set_piece_at_position(position=position, piece=Piece(player=player))
        position = Position(x=position.x+direction.dx, y=position.y+direction.dy) # need to make this a function - static function
    board.set_piece_at_position(position=position, piece=Piece(player=player))
