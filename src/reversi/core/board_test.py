from unittest import TestCase

from .board import Board, Piece, Player, make_board, Position

# Not using because flake complains
# from .board import *  # using this form because I consider this an extension of the board file. Right perspective?


# TODO(ope): create an extension that will create test scaffolding given a class
# need to do s?
class BoardTests(TestCase):

    def setUp(self):
        self.board_size = 4
        self.board = make_board(board_size=self.board_size)  # this is tested below and works as far as I can tell


class SizeTest(BoardTests):

    def test_size(self):
        assert (
            self.board_size
            == self.board.size
        )


class GetPieceAtPositionTest(BoardTests):

    def test_get_piece_at_position_none(self):
        assert (
            None
            is self.board.get_piece_at_position(position=Position(0, 0))
        )

    def test_get_piece_at_position_piece(self):
        assert (
            Piece(Player.ONE)
            == self.board.get_piece_at_position(position=Position(1, 1))
        )


class SetPieceAtPosition(BoardTests):

    def test_set_piece_at_position_piece(self):
        # haha, this breaks my assert at the end approach
        assert self.board.get_piece_at_position(position=Position(0, 0)) is None
        self.board.set_piece_at_position(position=Position(0, 0), piece=Piece(Player.ONE))
        assert (
            Piece(Player.ONE)
            == self.board.get_piece_at_position(position=Position(1, 1))
        )


class MakeBoardTests(TestCase):

    # TODO(ope)
    # going to write extension so I can do remove the test prefix
    def test_board_size_4(self):
        assert (
            make_board(board_size=4)
            == Board(
                pieces=[
                    [None, None, None, None],
                    [None, Piece(Player.ONE), Piece(Player.TWO), None],
                    [None, Piece(Player.TWO), Piece(Player.ONE), None],
                    [None, None, None, None],
                ]
            )
        )

    def test_board_size_5(self):
        assert (
            make_board(board_size=5)
            == Board(
                pieces=[
                    [None, None, None, None, None],
                    [None, Piece(Player.ONE), Piece(Player.TWO), None, None],
                    [None, Piece(Player.TWO), Piece(Player.ONE), None, None],
                    [None, None, None, None, None],
                    [None, None, None, None, None],
                ]
            )
        )

    def test_board_size_6(self):
        assert (
            make_board(board_size=6)
            == Board(
                pieces=[
                    [None, None, None, None, None, None],
                    [None, None, None, None, None, None],
                    [None, None, Piece(Player.ONE), Piece(Player.TWO), None, None],
                    [None, None, Piece(Player.TWO), Piece(Player.ONE), None, None],
                    [None, None, None, None, None, None],
                    [None, None, None, None, None, None],
                ]
            )
        )
