"""Class implementing an artificial intelligence to play the game."""
from code.game import board
from ..game import Player, Board, Action
from typing import List, Optional
import time

class AI(Player):
    max_depth: int
    times_iterated: int


    def __init__(self, white: bool, max_depth: int) -> None:
        super().__init__(white)
        self.max_depth = max_depth

    def receive(self, board: Board) -> None:
        beginning = time.time()
        self.times_iterated = 0
        list_actions = board.actions()  # get the list of possible actions
        eval_score = 0
        evalmax = 0
        for a in list_actions:  # for each possible action compute the evaluation value
            eval_score = self.alpha_beta_pruning(
                Board.board_from_move(board, a), 0, float('-inf'), float('inf'), True)
            if eval_score > evalmax:  # if it's the best value
                evalmax = eval_score
                best_action = a  # we can take this action which is the best

        if board.receive(best_action):  # Send to the board the best action
            print("IA move")
        else:
            raise Exception("Board has not accepted move by the AI.")
        print("Best move: "+str(evalmax)+" with: ["+str(best_action.x)+","+str(best_action.y)+"] dir: "+str(best_action.direction))
        print("Times iterated through: "+str(self.times_iterated))
        end = time.time()
        print("Time taken for depth: "+str(self.max_depth)+" is: "+str(end - beginning)+" seconds.")


    def alpha_beta_pruning(self, node: Board, current_depth: int, alpha: int, beta: int, maximizingPlayer: bool) -> int:
        self.times_iterated += 1
        """Alpha beta pruning implementation."""
        # if node is a leaf node return evaluation value of the node
        if current_depth == self.max_depth or node.terminal_state():
            return self.eval(node)

        if maximizingPlayer:  # max part of the minimax
            maxvalue = float('-inf')
            # for each child of the node (I don't know how to write this part)
            for action in node.actions():
                value = self.alpha_beta_pruning(
                    Board.board_from_move(node, action), current_depth+1, alpha, beta, False)
                maxvalue = max(maxvalue, value)
                alpha = max(alpha, maxvalue)
                if beta <= alpha:
                    break
            return maxvalue
        else:
            minvalue = float('inf')  # min part of the minimax
            # for each child of the node (I don't know how to write this part)
            for action in node.actions():
                value = self.alpha_beta_pruning(
                    Board.board_from_move(node, action), current_depth+1, alpha, beta, True)
                minvalue = min(minvalue, value)
                beta = min(beta, minvalue)
                if beta <= alpha:
                    break
            return minvalue

    def eval(self, state: Board) -> int:
        start = time.time()
        """Evaluate a state for a the player."""
        scores = state.calculate_players_total_block_size()
        if state.terminal_state():
            if self.white and scores[0] > scores[1] or not self.white and scores[0] < scores[1]:
                return float('inf')
            elif scores[0] == scores[1]:
                return 0
            return float('-inf')
        openness_player = state.openness(self.white)
        openness_opponent = state.openness(not self.white)
        score_player = scores[self.white]
        score_opponent = scores[not self.white]
        end = time.time()
        #print("Eval time taken:"+str(end-start))
        return (score_player - score_opponent) + (openness_player - openness_opponent)

    def result(self, action: Action) -> Board:

        return state
