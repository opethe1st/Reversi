from unittest import TestCase

from reversi.core.board import Board, Colours
from reversi.core.logic import (
    _compute_valid_move,
    _get_positions_with_colour,
    compute_score,
    compute_valid_moves,
    play_move
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
        expected_moves = {
            Position(1, 0): [(Position(1, 2), Directions.NORTH)],
            Position(0, 1): [(Position(2, 1), Directions.EAST)],
            Position(2, 3): [(Position(2, 1), Directions.SOUTH)],
            Position(3, 2): [(Position(1, 2), Directions.WEST)],
        }
        self.assertDictEqual(valid_moves, expected_moves)

    def test_simple_case_black(self):
        valid_moves = compute_valid_moves(board=self.board, colour=Colours.BLACK)
        expected_moves = {
            Position(1, 3): [(Position(1, 1), Directions.SOUTH)],
            Position(3, 1): [(Position(1, 1), Directions.WEST)],
            Position(2, 0): [(Position(2, 2), Directions.NORTH)],
            Position(0, 2): [(Position(2, 2), Directions.EAST)],
        }
        self.assertDictEqual(valid_moves, expected_moves)

    def test_single_piece(self):
        board_rep = "\n".join([
            '    ',
            ' W  ',
            '    ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.WHITE)
        expected_moves = dict()
        self.assertDictEqual(valid_moves, expected_moves)

    def test_single_piece_different_colours(self):
        board_rep = "\n".join([
            '    ',
            ' B  ',
            '    ',
            '    ',

        ])
        pieces = construct_pieces(board_rep)
        valid_moves = compute_valid_moves(board=Board(pieces), colour=Colours.WHITE)
        expected_moves = dict()
        self.assertDictEqual(valid_moves, expected_moves)


class TestGetPositionsWithColour(LogicTestCase):

    def test_basic(self):
        positions = _get_positions_with_colour(board=self.board, colour=Colours.WHITE)
        expected_positions = {Position(1, 2), Position(2, 1)}


class TestComputeValidMove(LogicTestCase):

    def test_basic(self):  # :)
        valid_move = _compute_valid_move(
            position=Position(1, 1),
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
            position=Position(1, 1),
            direction=Directions.SOUTH,
            board=board,
            colour=Colours.BLACK
        )
        self.assertFalse(valid_move)

    def test_basic_3(self):  # :)
        valid_move = _compute_valid_move(
            position=Position(1, 2),
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


class TestPlayMove(LogicTestCase):

    def test_black_plays_valid_move(self):
        play_move(board=self.board, position=Position(3, 1), colour=Colours.BLACK)
        expected_board = Board(
            construct_pieces(
                "\n".join([
                    '    ',
                    ' BW ',
                    ' BB ',
                    ' B  ',
                ])
            )
        )
        self.assertEqual(
            self.board,
            expected_board
        )

    def test_black_plays_valid_move_2(self):
        play_move(board=self.board, position=Position(1, 3), colour=Colours.BLACK)
        expected_board = Board(
            construct_pieces(
                "\n".join([
                    '    ',
                    ' BBB',
                    ' WB ',
                    '    ',
                ])
            )
        )
        self.assertEqual(
            self.board,
            expected_board
        )

    def test_white_plays_valid_move(self):
        play_move(board=self.board, position=Position(3, 2), colour=Colours.WHITE)
        expected_board = Board(
            construct_pieces(
                "\n".join([
                    '    ',
                    ' BW ',
                    ' WW ',
                    '  W ',
                ])
            )
        )
        self.assertEqual(
            self.board,
            expected_board
        )

    def test_white_plays_valid_move_2(self):
        play_move(board=self.board, position=Position(0, 1), colour=Colours.WHITE)
        expected_board = Board(
            construct_pieces(
                "\n".join([
                    ' W  ',
                    ' WW ',
                    ' WB ',
                    '    ',
                ])
            )
        )
        self.assertEqual(
            self.board,
            expected_board
        )

    def test_play_moves(self):
        play_move(board=self.board, position=Position(0, 1), colour=Colours.WHITE)
        play_move(board=self.board, position=Position(0, 2), colour=Colours.BLACK)
        expected_board = Board(
            construct_pieces(
                "\n".join([
                    ' WB ',
                    ' WB ',
                    ' WB ',
                    '    ',
                ])
            )
        )
        self.assertEqual(
            self.board,
            expected_board
        )
