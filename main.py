# Main file for the project. Contains the game loop.
from code.game import Board, Human

if __name__ == "main.py":
    board = Board()
    white = Player(white=True)
    black = Player(white=False)
    while board.continue():
        pass
