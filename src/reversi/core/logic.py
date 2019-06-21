from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Union
from itertools import cycle
from .board import Board, Colours, Piece
from .position import Directions, Position


# should be here or should it be in board.py?
def compute_valid_moves(board: Board, colour: Colours) -> Dict[Position, List[Tuple[Position, Directions]]]:
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


def _get_positions_with_colour(board: Board, colour: Colours) -> Set[Position]:
    return {position for position, piece in board if piece and piece.colour == colour}


def _compute_valid_move(position: Position, direction: Directions, board: Board, colour: Colours) -> Union["False", Position]:
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


def compute_score(board: Board) -> int:
    return Counter([piece.colour for _, piece in board if piece])


# TODO(ope): Colour everywhere should be Player
def play_move(board: Board, position: Position, colour: Colours) -> bool:
    # This violates CQRS?
    '''modifies board and returns True if this is a valid move'''
    moves = compute_valid_moves(board=board, colour=colour)
    if position not in moves:
        return False
    for origin, direction in moves[position]:
        _capture_pieces(start=origin, end=position, direction=direction, colour=colour, board=board)
    return True


def _capture_pieces(start: int, end: int, direction: Directions, colour: Colours, board: Board):
    position = start
    while position != end:
        board.set_piece_at_position(position=position, piece=Piece(colour=colour))
        position = Position(x=position.x+direction.dx, y=position.y+direction.dy) # need to make this a function - static function
    board.set_piece_at_position(position=position, piece=Piece(colour=colour))


def is_game_over(board):
    return all(not(compute_valid_moves(board=board, colour=colour)) for colour in Colours.ALL)


def print_board(board):
    def print_row(row):
        line = '|'
        colour_to_symbol = {
            Colours.WHITE: 'W',
            Colours.BLACK: 'B',
        }
        for piece in row:
            if piece is None:
                line += ' '
            else:
                line += colour_to_symbol[piece.colour]
        line += '|'
        print(line)

    print(' ----')
    for row in board._pieces:
        print_row(row)
    print(' ----')
    print()


def play_game():
    players = [Colours.BLACK, Colours.WHITE]
    board = Board(
        [
            [None, None, None, None],
            [None, Piece(Colours.WHITE), Piece(Colours.BLACK), None],
            [None, Piece(Colours.BLACK), Piece(Colours.WHITE), None],
            [None, None, None, None],
        ]
    )
    for player in cycle(players):
        if is_game_over(board):
            print(compute_score(board))
            break
        print_board(board)
        if compute_valid_moves(board, player):
            x, y = input(f"It is player: {player}'s turn. Input a position to move to: ").split()
            #  should also check if there is a invalid move and prompt player to retry or hint on what the valid moves are.
            play_move(board=board, position=Position(int(x), int(y)), colour=player)
        else:
            print(f"Skipped player: {player}'s turn since they have no valid move")


if __name__ == '__main__':
    play_game()
