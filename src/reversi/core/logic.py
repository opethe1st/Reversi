from .board import Board, Colours
from .position import Position, Directions


#  should be here or should it be in board.py?
def compute_valid_moves(board: Board, colour: Colours):
    colour_positions = _get_positions_with_colour(board=board, colour=colour)
    valid_moves = set()
    for colour_position in colour_positions:
        for direction in Directions.ALL:
            valid_move_for_piece = _compute_valid_move(
                colour_position=colour_position,
                direction=direction,
                board=board,
                colour=colour
            )
            if valid_move_for_piece:
                valid_moves.add(valid_move_for_piece)
    return valid_moves


def _get_positions_with_colour(board, colour):
    return {position for position, piece in board if piece and piece.colour is colour}


def _compute_valid_move(colour_position, direction, board, colour):
    other_colour_seen = False
    current_position = colour_position
    valid_moves = set()
    # woah, just found out about this! you can efficiently check ranges with 4 in range(123)!
    while (current_position.x in range(board.size)) and (current_position.y in range(board.size)):
        current_piece = board.get_piece_at_position(position=current_position)
        if other_colour_seen and current_piece is None:
            return current_position
        elif current_piece is not None and current_piece.colour != colour:
            other_colour_seen = True
        current_position = Position(x=current_position.x+direction.dx, y=current_position.y+direction.dy)
    return False
