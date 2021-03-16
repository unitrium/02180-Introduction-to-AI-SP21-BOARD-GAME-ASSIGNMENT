# Main file for the project. Contains the game loop.
from code.game import Board, Human

if __name__ == "__main__":
    board = Board(11)
    #Just for some testing, we don't have to have this in the end if it's always AI.
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


    #ASSUMPTION: AI WILL FIND OUT MOVE UPON RECEIVING .receive()?
    while not board.terminal_state():
        # Main file for the project. Contains the game loop.
        white.receive(board.state)
        print("Whites turn.")
        possible_actions = board.actions()
        if type(white) is Human:
            action = None
            white.display(board.state)
            #Endless loop because player is not using object Action(x,y,dir), but the board.actions() does.
            while not (action in possible_actions):
                action = white.ask_action()
        if board.terminal_state():
            break
        print("Blacks turn.")
        black.receive(board.state)
        possible_actions = board.actions()
        if black is Human:
            action = None
            black.display(board.state)
            while action not in possible_actions:
                action = black.ask_action()

    board._check_winner(board.state)
