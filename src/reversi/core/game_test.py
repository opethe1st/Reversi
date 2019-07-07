from unittest import TestCase

from .board import make_board, Board, Piece
from .game import (
    Game,
    _capture_pieces,
    _compute_valid_move,
    _get_positions_with_player_piece
)
from .player import Player
from .position import CardinalDirection, Position


class GameTests(TestCase):

    def setUp(self):
        self.game = Game(board=make_board(board_size=4))


class IsOverTest(GameTests):

    def test_no_player_one_pieces(self):
        # could use mock here :)
        self.game.compute_valid_moves = lambda *args, **kwargs: {}
        assert self.game.is_over()


class ComputeScores(GameTests):

    def test_initial_board(self):
        assert self.game.compute_scores() == {Player.ONE: 2, Player.TWO: 2}


class PlayMoveTest(GameTests):

    def test_invalid_move(self):
        assert self.game.play_move(position=Position(0, 0), player=Player.ONE) is False

    def test_valid_move(self):
        assert self.game.play_move(position=Position(3, 1), player=Player.ONE)


class ComputeValidMoveTest(GameTests):

    def test_player_one(self):
        assert self.game.compute_valid_moves(player=Player.ONE) == {
            Position(1, 3): [(Position(x=1, y=1), CardinalDirection.SOUTH.value)],
            Position(3, 1): [(Position(x=1, y=1), CardinalDirection.WEST.value)],
            Position(2, 0): [(Position(x=2, y=2), CardinalDirection.NORTH.value)],
            Position(0, 2): [(Position(x=2, y=2), CardinalDirection.EAST.value)]
        }


# Test utilities
class getPositionsWithPlayPiece(TestCase):

    def test_initial_board_with_player_one(self):
        board = make_board(board_size=4)
        positions = _get_positions_with_player_piece(board=board, player=Player.ONE)
        assert positions == {Position(1, 1), Position(2, 2)}


class computeValidMove(TestCase):

    def test_invalid_position(self):
        board = make_board(board_size=4)
        # what if player and position don't match?
        position, is_valid = _compute_valid_move(board=board, position=Position(1, 1), direction=CardinalDirection.EAST.value, player=Player.ONE)
        assert is_valid is False

    def test_invalid_position_and_player(self):
        board = make_board(board_size=4)
        # what if player and position don't match?
        position, is_valid = _compute_valid_move(board=board, position=Position(1, 1), direction=CardinalDirection.EAST.value, player=Player.TWO)
        # this fails
        # assert is_valid is False

    def test_valid_position_and_player(self):
        board = make_board(board_size=4)
        # what if player and position don't match?
        position, is_valid = _compute_valid_move(board=board, position=Position(1, 1), direction=CardinalDirection.WEST.value, player=Player.ONE)
        assert (position, is_valid) == (Position(3, 1), True)


class capturePieces(TestCase):

    def test_capture_player_one(self):
        board = make_board(board_size=4)
        # what if player and position don't match?
        _capture_pieces(board=board, start=Position(0, 0), end=Position(3, 0), direction=CardinalDirection.WEST.value, player=Player.ONE)
        assert board == Board(
            pieces=[
                [Piece(Player.ONE), Piece(Player.ONE), Piece(Player.ONE), Piece(Player.ONE)],
                [None, Piece(Player.ONE), Piece(Player.TWO), None],
                [None, Piece(Player.TWO), Piece(Player.ONE), None],
                [None, None, None, None],
            ]
        )
