# Class for the board of the game
from typing import List, Optional, Tuple

from .player import Player


class Board:
    """A board the players can interact with.
    Initially empty.
    """
    state: List[List[Optional[int]]]

    def __init__(self) -> None:
        pass

    def send(self, player: Player) -> None:
        """Send the state of the board to the player."""
        player.receive(self.state)

    def receive(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Receive a move from a player."""
        pass

    def check_continue(self) -> bool:
        """Whether a move is still possible."""
        pass

    def _check_integrity(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Whether a move is acceptable by the current board."""
        pass
