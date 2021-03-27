import pytest
from ..game import Board, Human, Action
from ..ai import AI


def test_basic_create():
    board = Board(size=7)
    player_1 = Human(white=True)
    player_2 = AI(white=False, max_depth=10)


def test_actions():
    """Test that the board returns the correct list of possible actions."""
    board = Board(size=7)
    actions = board.actions()
    assert len(actions) == 5*5*4 + 5*4*3 + 4*2
    assert actions[0].x == 0
    assert actions[0].y == 0
    assert actions[0].direction == 1


def test_copy():
    board = Board(size=7)
    board.receive(Action(1, 1, 1))
    board2 = board.__copy__()
    board2.receive(Action(4, 4, 0))
    assert board.state[4][4] is None
    assert board2.state[4][4] == 0
