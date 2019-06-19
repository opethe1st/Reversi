from unittest import TestCase

from reversi.core.board import Board, Colours
from reversi.core.logic import (
    _compute_valid_move,
    _get_positions_with_colour,
    compute_score,
    compute_valid_moves
)
from reversi.core.position import Directions, Position
from tests.utils import construct_pieces


class LogicTestCase(TestCase):

    def setUp(self):
        board_rep = "\n".join([
            '    ',
            ' BW ',
            ' WB ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        self.board = Board(pieces)

class TestComputeValidMoves(LogicTestCase):

    def test_simple_case_white(self):
        valid_moves = compute_valid_moves(board=self.board, colour=Colours.WHITE)
        expected_moves = set([
            Position(1, 0),
            Position(0, 1),
            Position(2, 3),
            Position(3, 2),
        ])
        self.assertSetEqual(valid_moves, expected_moves)

    def test_simple_case_black(self):
        valid_moves = compute_valid_moves(board=self.board, colour=Colours.BLACK)
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


class TestGetPositionsWithColour(LogicTestCase):

    def test_basic(self):
        positions = _get_positions_with_colour(board=self.board, colour=Colours.WHITE)
        expected_positions = {Position(1, 2), Position(2, 1)}


class TestComputeValidMove(LogicTestCase):

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


class TestScore(LogicTestCase):

    def test_score(self):
        score = compute_score(self.board)
        expected_score = {Colours.BLACK: 2, Colours.WHITE: 2}
        self.assertDictEqual(score, expected_score)
