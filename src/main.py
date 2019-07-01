import itertools

from reversi.core import Game, Player, make_board
from reversi.view.pygame_ui import PygameUI


def run(board_size=4):
    board = make_board(board_size=board_size)
    game = Game(board=board)
    ui = PygameUI(board=board)

    ui.display_board()

    for player in itertools.cycle(Player):
        if game.is_over():
            ui.display_game_over()
            ui.display_scores(scores=game.compute_scores())

        # what if the move if coming over the internet?
        position, was_clicked = ui.get_move(player=player)
        if was_clicked:
            game.play_move(player=player, position=position)
            ui.display_scores(scores=game.compute_scores())

        ui.display_board()


if __name__ == '__main__':
    run(board_size=6)
