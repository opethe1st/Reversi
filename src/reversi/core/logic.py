from collections import Counter, defaultdict

from .board import Board, Colours, Piece
from .position import Directions, Position


# should be here or should it be in board.py?
def compute_valid_moves(board: Board, colour: Colours):
    positions = _get_positions_with_colour(board=board, colour=colour)
    moves = defaultdict(list)
    for position in positions:
        for direction in Directions.ALL:
            valid_position = _compute_valid_move(
                position=position,
                direction=direction,
                board=board,
                colour=colour
            )
            if valid_position:
                moves[valid_position].append((position, direction))
    return moves


def _get_positions_with_colour(board, colour):
    return {position for position, piece in board if piece and piece.colour == colour}


def _compute_valid_move(position, direction, board, colour):
    other_colour_seen = False
    current_position = position
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


def compute_score(board):
    return Counter([piece.colour for _, piece in board if piece])


def play_move(board, position, colour): # TODO(ope): Colour everywhere should be Player\
    # This violates CQRS?
    '''modifies board and returns True if this is a valid move'''
    moves = compute_valid_moves(board=board, colour=colour)
    for origin, direction in moves[position]:
        _capture_pieces(start=origin, end=position, direction=direction, colour=colour, board=board)
    return True


def _capture_pieces(start, end, direction, colour, board):
    position = start
    while position != end:
        board.set_piece_at_position(position=position, piece=Piece(colour=colour))
        position = Position(x=position.x+direction.dx, y=position.y+direction.dy) # need to make this a function - static function
    board.set_piece_at_position(position=position, piece=Piece(colour=colour))
