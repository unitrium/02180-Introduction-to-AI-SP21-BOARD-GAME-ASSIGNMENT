import pytest

from ..game import Board, Human


def test_basic_create():
    board = Board()
    player_1 = Human(white=True)
    player_2 = Human(white=False)
