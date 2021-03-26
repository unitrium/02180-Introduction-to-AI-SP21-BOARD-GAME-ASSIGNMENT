"""Measures the performance of two AI playing against one another in terms of time to make a decision."""
from time import time
from code.game import Board
from code.ai import AI

board = Board(11)
player_1 = AI(white=True, max_depth=1)
player_2 = AI(white=False, max_depth=1)
turncount = 1
print("Start")
while not board.terminal_state():
    if turncount % 2 == 1:
        print("Player 1")
        start_1 = time()
        board.send(player_1)
        print(f"Player 1 took {time() - start_1}s")
        white_turn = False
    else:
        print("Player 2")
        start_2 = time()
        board.send(player_2)
        print(f"Player 2 took {time() - start_2}s")
        white_turn = True
    turncount += 1
