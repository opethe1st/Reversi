from unittest import TestCase

from reversi.core.board import Board, Player
from reversi.core.game import (
    _compute_valid_move,
    _get_positions_with_player_piece,
)
from reversi.core.position import CardinalDirection, Position
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

# class TestComputeValidMoves(LogicTestCase):

#     def test_simple_case_white(self):
#         valid_moves = compute_valid_moves(board=self.board, player=Player.ONE)
#         expected_moves = {
#             Position(1, 0): [(Position(1, 2), CardinalDirection.NORTH)],
#             Position(0, 1): [(Position(2, 1), CardinalDirection.EAST)],
#             Position(2, 3): [(Position(2, 1), CardinalDirection.SOUTH)],
#             Position(3, 2): [(Position(1, 2), CardinalDirection.WEST)],
#         }
#         self.assertDictEqual(valid_moves, expected_moves)

#     def test_simple_case_black(self):
#         valid_moves = compute_valid_moves(board=self.board, player=Player.TWO)
#         expected_moves = {
#             Position(1, 3): [(Position(1, 1), CardinalDirection.SOUTH)],
#             Position(3, 1): [(Position(1, 1), CardinalDirection.WEST)],
#             Position(2, 0): [(Position(2, 2), CardinalDirection.NORTH)],
#             Position(0, 2): [(Position(2, 2), CardinalDirection.EAST)],
#         }
#         self.assertDictEqual(valid_moves, expected_moves)

#     def test_single_piece(self):
#         board_rep = "\n".join([
#             '    ',
#             ' W  ',
#             '    ',
#             '    ',

#         ])
#         pieces = construct_pieces(board_rep)
#         valid_moves = compute_valid_moves(board=Board(pieces), player=Player.ONE)
#         expected_moves = dict()
#         self.assertDictEqual(valid_moves, expected_moves)

#     def test_single_piece_different_Player(self):
#         board_rep = "\n".join([
#             '    ',
#             ' B  ',
#             '    ',
#             '    ',

#         ])
#         pieces = construct_pieces(board_rep)
#         valid_moves = compute_valid_moves(board=Board(pieces), player=Player.ONE)
#         expected_moves = dict()
#         self.assertDictEqual(valid_moves, expected_moves)


class TestGetPositionsWithplayer(LogicTestCase):

    def test_basic(self):
        positions = _get_positions_with_player_piece(board=self.board, player=Player.ONE)
        expected_positions = {Position(1, 2), Position(2, 1)}
        self.assertEqual(positions, expected_positions)


class TestComputeValidMove(LogicTestCase):

    def test_basic(self):  # :)
        valid_move = _compute_valid_move(
            position=Position(1, 1),
            direction=CardinalDirection.SOUTH,
            board=self.board,
            player=Player.TWO
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
            direction=CardinalDirection.SOUTH,
            board=board,
            player=Player.TWO
        )
        self.assertFalse(valid_move)

    def test_basic_3(self):  # :)
        valid_move = _compute_valid_move(
            position=Position(1, 2),
            direction=CardinalDirection.NORTH,
            board=self.board,
            player=Player.ONE
        )
        self.assertEqual(Position(1, 0), valid_move)


# class TestScore(LogicTestCase):

#     def test_score(self):
#         score = compute_score(self.board)
#         expected_score = {Player.TWO: 2, Player.ONE: 2}
#         self.assertDictEqual(score, expected_score)


# class TestPlayMove(LogicTestCase):

#     def test_black_plays_valid_move(self):
#         play_move(board=self.board, position=Position(3, 1), player=Player.TWO)
#         expected_board = Board(
#             construct_pieces(
#                 "\n".join([
#                     '    ',
#                     ' BW ',
#                     ' BB ',
#                     ' B  ',
#                 ])
#             )
#         )
#         self.assertEqual(
#             self.board,
#             expected_board
#         )

#     def test_black_plays_valid_move_2(self):
#         play_move(board=self.board, position=Position(1, 3), player=Player.TWO)
#         expected_board = Board(
#             construct_pieces(
#                 "\n".join([
#                     '    ',
#                     ' BBB',
#                     ' WB ',
#                     '    ',
#                 ])
#             )
#         )
#         self.assertEqual(
#             self.board,
#             expected_board
#         )

#     def test_white_plays_valid_move(self):
#         play_move(board=self.board, position=Position(3, 2), player=Player.ONE)
#         expected_board = Board(
#             construct_pieces(
#                 "\n".join([
#                     '    ',
#                     ' BW ',
#                     ' WW ',
#                     '  W ',
#                 ])
#             )
#         )
#         self.assertEqual(
#             self.board,
#             expected_board
#         )

#     def test_white_plays_valid_move_2(self):
#         play_move(board=self.board, position=Position(0, 1), player=Player.ONE)
#         expected_board = Board(
#             construct_pieces(
#                 "\n".join([
#                     ' W  ',
#                     ' WW ',
#                     ' WB ',
#                     '    ',
#                 ])
#             )
#         )
#         self.assertEqual(
#             self.board,
#             expected_board
#         )

#     def test_play_moves(self):
#         play_move(board=self.board, position=Position(0, 1), player=Player.ONE)
#         play_move(board=self.board, position=Position(0, 2), player=Player.TWO)
#         expected_board = Board(
#             construct_pieces(
#                 "\n".join([
#                     ' WB ',
#                     ' WB ',
#                     ' WB ',
#                     '    ',
#                 ])
#             )
#         )
#         self.assertEqual(
#             self.board,
#             expected_board
#         )
