# Class for the board of the game
from typing import List, Optional, Tuple

from .player import Player


class Action:
    x: int
    y: int
    direction: int

    def __init__(self, x: int, y: int, direction: int) -> None:
        self.x = x
        self.y = y
        self.direction = direction


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

    def terminal_state(self) -> bool:
        """Determine whether the game is over."""
        return len(self.actions()) == 0

    def _check_integrity(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Whether a move is acceptable by the current board."""
        direction = move[1]
        x = move[0][0]
        y = move[0][1]

        if not self.state[x][y] is None:
            return False
        if direction not in self._free_neighbors():
            return False
        return True

    def actions(self) -> List[Action]:
        """Computes all the possible actions."""
        actions = []
        for y, line in enumerate(self.state):
            for x, tile in enumerate(line):
                if tile is None:
                    for direction in self._free_neighbors(x, y):
                        actions.append(Action(x, y, direction))
        return actions

    def _free_neighbors(self, x: int, y: int) -> List[int]:
        """Returns the free adjacents directions 0 up, 1 right, 2 down, 3 left."""
        neighbors = []
        if not y == 0 and self.state[x][y-1] is None:
            neighbors.append(0)
        if not x == (self.size - 1) and self.state[x+1][y] is None:
            neighbors.append(1)
        if not y == (self.size - 1) and self.state[x][y+1] is None:
            neighbors.append(2)
        if not x == 0 and self.state[x-1][y] is None:
            neighbors.append(3)
        return neighbors
