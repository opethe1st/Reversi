from itertools import cycle

from reversi import Game
from reversi.view.cli import SimpleCLI

if __name__ == '__main__':
    game = Game()
    game.play_game(ui=SimpleCLI())
    # is this better as?
    # game = Game(ui=SimpleCLI())
    # game.play_game()
    # or
    # game.run()
    # or
    # play_game(game=Game(), ui=SimpleCLI())
