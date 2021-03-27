""" Main file for the project. Contains the game loop."""
from code.game import Board, Human
from code.ai import AI

if __name__ == "__main__":
    board = Board(11)
    # Just for some testing, we don't have to have this in the end if it's always AI.
    ai_response = ""
    while ai_response != "YES" and ai_response != "NO":
        ai_response = str(input("Would you like to play with an AI? YES/NO"))
    color = ""
    while color != "BLACK" and color != "WHITE":
        color = str(input("Would you like to be BLACK or WHITE?"))
    white = None
    black = None
    if color == "BLACK":
        black = Human(white=False)
    else:
        white = Human(white=True)
    if ai_response == "YES":
        if color == "BLACK":
            white = AI(white=True, max_depth=3)
        else:
            black = AI(white=False, max_depth=3)
    else:
        if color == "BLACK":
            white = Human(white=True)
        else:
            black = Human(white=False)

    # Using turn logic as described in analysis. turncount mod 2 = 1 means white turn, else black.
    turncount = 1
    while not board.terminal_state():
        if turncount % 2 == 1:
            print("White turn.")
            board.send(white)
            white_turn = False
        else:
            print("Black turn.")
            board.send(black)
            white_turn = True
        turncount += 1

    board.declare_winner()
