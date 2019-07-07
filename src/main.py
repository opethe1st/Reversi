import sys

import pygame  # I dont like that the fact that I am using pygame is leaking but I can't think of an alternative
import pygame.locals

from reversi.core import Game, Player, Position, make_board
from reversi.view import GUI
from reversi.core import next_player


def run(board_size=4):

    board = make_board(board_size=board_size)
    game = Game(board=board)
    ui = GUI(board=board)

    player = Player.ONE

    ui.display_board()
    ui.display_score_board(scores=game.compute_scores(), player_to_play=player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                # it is pos[1] corresponds to the x coordinate and pos[0] corresponds to the y-coordinate
                position, was_clicked = ui.get_clicked_ball(position=Position(x=event.pos[1], y=event.pos[0]))
                if was_clicked:
                    is_valid_move = game.play_move(player=player, position=position)
                    if is_valid_move:
                        # TODO(ope): should I have a function that calls both of these functions at the same time?
                        ui.display_board()
                        player = next_player(player=player)
                        ui.display_score_board(scores=game.compute_scores(), player_to_play=player)
                    # if there are no valid moves for the next player, skip their turn
                    if not game.compute_valid_moves(player=player):
                        player_to_play = next_player(player=player)
                        ui.display_skip_move(skipped_player=player, player_to_play=player_to_play)
                        player = player_to_play

        if game.is_over():
            ui.display_game_over(scores=game.compute_scores())


if __name__ == '__main__':
    run(board_size=8)
