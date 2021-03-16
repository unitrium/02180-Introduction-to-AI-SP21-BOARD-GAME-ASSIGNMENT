import pytest

from ..game import Board, Human


def test_basic_create():
    board = Board(size=7)
    player_1 = Human(white=True)
    player_2 = Human(white=False)


def test_actions():
    """Test that the board returns the correct list of possible actions."""
    board = Board(size=7)
    actions = board.actions()
    assert len(actions) == 5*5*4 + 5*4*3 + 4*2
    assert actions[0].x == 0
    assert actions[0].y == 0
    assert actions[0].direction == 1
