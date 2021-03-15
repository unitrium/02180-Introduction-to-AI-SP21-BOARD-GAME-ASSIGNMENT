"""Class for defining a player."""
from typing import List, Tuple
from abc import ABC, abstractmethod


class Player(ABC):
    """A player that can interact with a board."""
    white: bool

    def __init__(self, white: bool) -> None:
        self.white = white

    @abstractmethod
    def receive(self, state: List[List[int]]) -> None:
        """Receive the state of the board."""
        pass


class Human(Player):
    """A player who is also human."""

    def display(self, state: List[List[int]]) -> None:
        """Displays a state to the human when it's their turn.
        White tiles are represented by X, black tiles are
        represented by O."""
        print("Your turn, the board looks like this:")
        print()
        for line in state:
            printed_line = ""
            for col in line:
                if col is None:
                    printed_line += "  "
                elif col == 0:
                    printed_line += "X "
                else:
                    printed_line += "O "
            print(printed_line[0:-1])

    def ask_action(self) -> Tuple[Tuple[int, int], int]:
        """Asks the human for a move."""
        print("What is your move ?")
        x = int(input("Start by giving the x coordinate of the white part."))
        y = int(input("Now give the y coordinate of the white part."))
        direction = int(input(
            "The direction of the black part? 0 is up, 1 is right, 2 is down, 3 is left"))
        return ((x, y), direction)

    def receive(self, state: List[List[int]]) -> None:
        return super().receive(state)
