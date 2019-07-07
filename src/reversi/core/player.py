from enum import Enum


# TODO(ope): move to constants.py?
class Player(Enum):
    ONE = 'ONE'
    TWO = 'TWO'


def next_player(player):
    return Player.TWO if player == Player.ONE else Player.ONE
