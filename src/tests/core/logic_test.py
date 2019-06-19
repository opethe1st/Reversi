from unittest import TestCase

from tests.utils import construct_pieces

from reversi.core.board import Board, Colours
from reversi.core.logic import (
    _compute_valid_move,
    _get_positions_with_colour,
    compute_valid_moves
)
from reversi.core.position import Directions, Position


class TestComputeValidMoves(TestCase):

    def test_simple_case_white(self):
        board_rep = "\n".join([
            '    ',
            ' BW ',
            ' WB ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.WHITE)
        expected_moves = set([
            Position(1, 0),
            Position(0, 1),
            Position(2, 3),
            Position(3, 2),
        ])
        self.assertSetEqual(valid_moves, expected_moves)

    def test_simple_case_black(self):
        board_rep = "\n".join([
            '    ',
            ' BW ',
            ' WB ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.BLACK)
        expected_moves = set([
            Position(1, 3),
            Position(3, 1),
            Position(2, 0),
            Position(0, 2),
        ])
        self.assertSetEqual(valid_moves, expected_moves)

    def test_single_piece(self):
        board_rep = "\n".join([
            '    ',
            ' W  ',
            '    ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.WHITE)
        expected_moves = set()
        self.assertSetEqual(valid_moves, expected_moves)

    def test_single_piece_different_colours(self):
        board_rep = "\n".join([
            '    ',
            ' B  ',
            '    ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.WHITE)
        expected_moves = set()
        self.assertSetEqual(valid_moves, expected_moves)


class TestGetPositionsWithColour(TestCase):

    def test_basic(self):
        board_rep = "\n".join([
            '    ',
            ' BW ',
            ' WB ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        positions = _get_positions_with_colour(board=Board(pieces), colour=Colours.WHITE)
        expected_positions = {Position(1, 2), Position(2, 1)}


class TestComputeValidMove(TestCase):

    def setUp(self):
        board_rep = "\n".join([
            '    ',
            ' BW ',
            ' WB ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        self.board = Board(pieces)

    def test_basic(self):  # :)
        valid_move = _compute_valid_move(
            colour_position=Position(1, 1),
            direction=Directions.SOUTH,
            board=self.board,
            colour=Colours.BLACK
        )
        self.assertEqual(Position(1, 3), valid_move)

    def test_basic_2(self):  # :)
        board_rep = "\n".join([
            '    ',
            ' B  ',
            '    ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        board = Board(pieces)
        valid_move = _compute_valid_move(
            colour_position=Position(1, 1),
            direction=Directions.SOUTH,
            board=board,
            colour=Colours.BLACK
        )
        self.assertFalse(valid_move)

    def test_basic_3(self):  # :)
        valid_move = _compute_valid_move(
            colour_position=Position(1, 2),
            direction=Directions.NORTH,
            board=self.board,
            colour=Colours.WHITE
        )
        self.assertEqual(Position(1, 0), valid_move)
