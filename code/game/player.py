"""Class for defining a player."""
from typing import List, Tuple
from abc import ABC, abstractmethod


class Action:
    x: int
    y: int
    direction: int

    def __init__(self, x: int, y: int, direction: int) -> None:
        self.x = x
        self.y = y
        self.direction = direction


class Player(ABC):
    """A player that can interact with a board."""
    white: bool

    def __init__(self, white: bool) -> None:
        self.white = white

    @abstractmethod
    def receive(self, board: "Board") -> None:
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
        print("  0 1 2 3 4 5 6 7 8 9 10")
        number = 0
        for line in state:
            printed_line = str(number)
            if number < 10:
                printed_line += " "
            for col in line:
                if col is None:
                    printed_line += "_ "
                elif col == 0:
                    printed_line += "X "
                else:
                    printed_line += "O "
            print(printed_line[0:-1])
            number += 1

    def ask_action(self) -> Action:
        """Asks the human for a move."""
        print("What is your move ?")
        x = int(input("Start by giving the x coordinate of the white part."))
        y = int(input("Now give the y coordinate of the white part."))
        direction = int(input(
            "The direction of the black part? 0 is up, 1 is right, 2 is down, 3 is left"))
        return Action(x, y, direction)

    def receive(self, board: "Board") -> None:
        move_accepted = False
        while not move_accepted:
            self.display(board.state)
            if board.receive(self.ask_action()):
                move_accepted = True
            else:
                print("Your move isn't possible. Please choose again.")
