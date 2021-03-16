# Main file for the project. Contains the game loop.
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
            white = AI(white=True)
        else:
            black = AI(white=False)
    else:
        if color == "BLACK":
            white = Human(white=True)
        else:
            black = Human(white=False)

    white_turn = True
    while not board.terminal_state():
        # Main file for the project. Contains the game loop.
        if white_turn:
            print("White turn.")
            board.send(white)
            white_turn = False
        else:
            print("Black turn.")
            board.send(black)
            white_turn = True

    board.declare_winner(board.state)
