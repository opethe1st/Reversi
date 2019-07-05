import sys

import pygame # I am going to delete this!
import pygame.locals # I am going to delete this too!

from reversi.core import Game, Player, make_board, Position
from reversi.view.pygame_ui import GUI


def run(board_size=4):
    board = make_board(board_size=board_size)
    game = Game(board=board)
    ui = GUI(board=board)

    ui.display_board()
    ui.display_scores(scores=game.compute_scores())

    player = Player.ONE
    next_player = lambda player: Player.TWO if player == Player.ONE else Player.ONE
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                ui.display_game_over()
                ui.display_scores(scores=game.compute_scores())
                pygame.quit()
                sys.exit()

            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                # I think there is real confusion with what is x and what is y
                position, was_clicked = ui.get_clicked_ball(position=Position(x=event.pos[0], y=event.pos[1]))
                if was_clicked:
                    is_valid_move = game.play_move(player=player, position=position)
                    ui.display_scores(scores=game.compute_scores())
                    ui.display_board()
                    if is_valid_move:
                        player = next_player(player=player)
                    if not game.compute_valid_moves(player=player):
                        player = next_player(player=player)
                        print('skipping this move because you have no valid moves')

                    print('next player: ', player)

        if game.is_over():
            ui.display_game_over()


if __name__ == '__main__':
    run(board_size=6)
