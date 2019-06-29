from dataclasses import dataclass, field
from typing import List

from reversi.utils import Enum

from .position import Position


class Player(Enum):
    ONE = 'ONE'
    TWO = 'TWO'


@dataclass
class Piece:
    player: Player


@dataclass
class Board:

    _pieces: List[List["Piece"]]

    def __post_init__(self):
        # TODO(ope): validate pieces
        pass

    def __iter__(self):
        for row_no, row in enumerate(self._pieces):
            for col_no, col in enumerate(row):
                yield Position(x=row_no, y=col_no), self._pieces[row_no][col_no]

    @property
    def size(self):
        return len(self._pieces)

    def get_piece_at_position(self, position):
        # TODO(ope): better error message here
        return self._pieces[position.x][position.y]

    def set_piece_at_position(self, position, piece):
        # TODO(ope): better error message here
        self._pieces[position.x][position.y] = piece

    # TODO(ope): maybe a repr here? - add one that has Player? or symbols?
