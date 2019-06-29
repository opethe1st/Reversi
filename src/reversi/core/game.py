from collections import Counter, defaultdict
from itertools import cycle
from typing import Dict, List, Set, Tuple, Union

from reversi.view import UI

from .board import Board, Piece, Player, PlayerType
from .position import CardinalDirection, Position


class Game:
    '''This class contains game rules'''

    def __init__(self):
        # for now, all boards start the same
        self._board = Board(
            [
                [None, None, None, None],
                [None, Piece(Player.ONE), Piece(Player.TWO), None],
                [None, Piece(Player.TWO), Piece(Player.ONE), None],
                [None, None, None, None],
            ]
        )

    # possibly move this out
    def play_game(self, ui: UI):
        players = [Player.TWO, Player.ONE]
        for player in cycle(players):
            score_counter = self.compute_score()
            if self.is_game_over():
                ui.display_game_over(score_counter={player: score_counter.get(player, 0) for player in players})
                break

            ui.display_board(board=self._board, score_counter=score_counter)
            if self.compute_valid_moves(player=player):  # need to address this mismatch between player and player
                x, y = ui.get_move(player)
                # should also check if there is a invalid move and prompt player to retry or hint on what the valid moves are.
                self.play_move(position=Position(x, y), player=player)
            else:
                ui.display_skip_move(player=player)

    # all of this should probably be private
    def is_game_over(self):
        return all(not(self.compute_valid_moves(player=player)) for player in Player.ALL)

    def compute_score(self) -> Counter:
        return Counter([piece.player for _, piece in self._board if piece])

    def play_move(self, position: Position, player: PlayerType) -> bool:
        # This violates CQRS?
        '''modifies board and returns True if this is a valid move'''
        moves = self.compute_valid_moves(player=player)
        if position not in moves:
            return False
        for origin, direction in moves[position]:
            _capture_pieces(start=origin, end=position, direction=direction, player=player, board=self._board)
        return True

    def compute_valid_moves(self, player: PlayerType) -> Dict[Position, List[Tuple[Position, CardinalDirection]]]:
        positions = _get_positions_with_player_piece(board=self._board, player=player)
        moves: Dict[Position, List] = defaultdict(list)
        for position in positions:
            for direction in CardinalDirection.ALL:  # type: ignore
                valid_position = _compute_valid_move(
                    position=position,
                    direction=direction,
                    board=self._board,
                    player=player
                )
                if valid_position:
                    moves[valid_position].append((position, direction))  # type: ignore
        return moves


def _get_positions_with_player_piece(board: Board, player: PlayerType) -> Set[Position]:
    return {position for position, piece in board if piece and piece.player == player}


# actually this should be Union[False, Position]
def _compute_valid_move(board: Board, position: Position, direction: CardinalDirection, player: PlayerType) -> Union[bool, Position]:
    '''return a valid position to move to, or False if there is None'''
    other_player_seen = False
    current_position = position
    # woah, just found out about this! you can efficiently check ranges with 4 in range(123)!
    while (current_position.x in range(board.size)) and (current_position.y in range(board.size)):
        current_piece = board.get_piece_at_position(position=current_position)
        if other_player_seen and current_piece is None:
            return current_position
        elif current_piece is not None and current_piece.player != player:
            other_player_seen = True
        current_position = _next_position_in_direction(position=current_position, direction=direction)
    return False


def _capture_pieces(board: Board, start: Position, end: Position, direction: CardinalDirection, player: PlayerType):
    position = start
    while position != end:
        board.set_piece_at_position(position=position, piece=Piece(player=player))
        position = _next_position_in_direction(position=position, direction=direction)
    # set piece at the end too.
    board.set_piece_at_position(position=position, piece=Piece(player=player))


def _next_position_in_direction(position, direction):
    return Position(x=position.x+direction.dx, y=position.y+direction.dy)
