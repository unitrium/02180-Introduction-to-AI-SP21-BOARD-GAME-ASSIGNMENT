# Class for the board of the game
from typing import List, Optional, Tuple

from .player import Player


class Board:
    """A board the players can interact with.
    Initially empty.
    """
    state: List[List[Optional[int]]]
    size: int

    def __init__(self, size: int) -> None:
        self.size = size
        self.state = [[None for _ in range(size)] for _ in range(size)]

    def send(self, player: Player) -> None:
        """Send the state of the board to the player."""
        player.receive(self.state)

    def receive(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Receive a move from a player."""
        if not self._check_integrity(move):
            return False
        direction = move[1]
        x = move[0][0]
        y = move[0][1]
        self.state[x][y] = 0
        if direction == 0:
            self.state[x][y+1] = 1
        elif direction == 1:
            self.state[x+1][y] = 1
        elif direction == 2:
            self.state[x][y-1] = 1
        else:
            self.state[x-1][y] = 1
        return False

    def check_continue(self) -> bool:
        """Whether a move is still possible."""
        pass

    def _check_integrity(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Whether a move is acceptable by the current board."""
        direction = move[1]
        x = move[0][0]
        y = move[0][1]
        if x >= self.size or x < 0 or y >= self.size or y < 0:
            return False
        if x == 0 and direction == 3:
            return False
        if y == 0 and direction == 0:
            return False
        if x == (self.size - 1) and direction == 1:
            return False
        if y == (self.size - 1) and direction == 2:
            return False
        return True
