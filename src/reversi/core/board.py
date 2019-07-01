from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from .player import Player
from .position import Position


@dataclass
class Piece:
    player: Player


class Board:

    def __init__(self, pieces: List[List[Optional[Piece]]]) -> None:
        self._pieces = pieces

    def __post_init__(self):
        # TODO(ope): validate pieces
        pass

    def __iter__(self) -> Iterable[Tuple[Position, Optional[Piece]]]:
        for row_no, row in enumerate(self._pieces):
            for col_no, col in enumerate(row):
                yield Position(x=row_no, y=col_no), self._pieces[row_no][col_no]

    @property
    def size(self) -> int:
        return len(self._pieces)

    def get_piece_at_position(self, position: Position) -> Optional[Piece]:
        # TODO(ope): better error message here
        return self._pieces[position.x][position.y]

    def set_piece_at_position(self, position: Position, piece: Piece) -> None:
        # TODO(ope): better error message here
        self._pieces[position.x][position.y] = piece

    # TODO(ope): maybe a repr here? - add one that has Player? or symbols?


# TODO(ope): make this work for different sizes
def make_board(board_size=4):
    return Board(
        [
            [None, None, None, None],
            [None, Piece(Player.ONE), Piece(Player.TWO), None],
            [None, Piece(Player.TWO), Piece(Player.ONE), None],
            [None, None, None, None],
        ]
    )
