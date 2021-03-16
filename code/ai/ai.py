"""Class implementing an artificial intelligence to play the game."""
from ..game import Player, Board


class AI(Player):
    def receive(self, board: Board) -> None:
        actions = board.actions()
        if not board.receive(actions[0]):
            raise Exception("Board has not accepted move by the AI.")
