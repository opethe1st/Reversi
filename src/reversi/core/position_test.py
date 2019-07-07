from unittest import TestCase

from .position import (
    CardinalDirection,
    Direction,
    Position,
    next_position_in_direction
)


class DirectionTests(TestCase):
    pass


class AddDirection(DirectionTests):

    #  very trivial test, I know, I know
    def test_direction_north_plus_west(self):
        direction = CardinalDirection.NORTH.value + CardinalDirection.EAST.value
        assert direction == Direction(dx=-1, dy=-1)


class NextPositionInDirection(TestCase):

    # possibly too trivial tests but simpler things have broken before :)
    def test_direction_west(self):
        position = next_position_in_direction(position=Position(0, 0), direction=CardinalDirection.NORTH.value)
        assert position == Position(0, -1)
