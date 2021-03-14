# Main file for the project. Contains the game loop.
from .game import Board, Player

if __name__ == "main.py":
    board = Board()
    white = Player(white=True)
    black = Player(white=False)
