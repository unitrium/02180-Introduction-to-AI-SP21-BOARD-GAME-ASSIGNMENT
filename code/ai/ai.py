"""Class implementing an artificial intelligence to play the game."""
from ..game import Player, Board, Action
from typing import List, Optional


class AI(Player):
    max_depth: int
    eval_score: int

    def __init__(self, white: bool, max_depth: int, eval_score: int) -> None:
        super().__init__(white)
        self.max_depth = max_depth
        self.eval_score = eval_score

    def receive(self, board: Board) -> None:

        list_actions = board.actions()  # get the list of possible actions
        eval_score = 0
        evalmax = 0
        for a in list_actions:  # for each possible action compute the evaluation value
            eval_score = self.alpha_beta_pruning(
                a, 0, float('-inf'), float('inf'), True)
            if eval_score > evalmax:  # if it's the best value
                evalmax = eval_score
                best_action = a  # we can take this action which is the best

        if board.receive(best_action):  # Send to the board the best action
            print("IA move")
        else:
            raise Exception("Board has not accepted move by the AI.")

    def alpha_beta_pruning(self, node, current_depth, alpha, beta, maximizingPlayer) -> int:
        self.max_depth = 20  # for the moment it's a random max_depth
        # if node is a leaf node return evaluation value of the node
        if current_depth == self.max_depth or self.board.terminal_state():
            e = self.evaluation_function(node)
            # print(e)
            return e

        if maximizingPlayer:  # max part of the minimax
            maxvalue = float('-inf')
            # for each child of the node (I don't know how to write this part)
            for child in node:
                value = self.alpha_beta_pruning(
                    child, current_depth+1, alpha, beta, False)
                maxvalue = max(maxvalue, value)
                alpha = max(alpha, maxvalue)
                if beta <= alpha:
                    break
            return maxvalue
        else:
            minvalue = float('inf')  # min part of the minimax
            # for each child of the node (I don't know how to write this part)
            for child in node:
                value = self.alpha_beta_pruning(
                    child, current_depth+1, alpha, beta, True)
                minvalue = min(minvalue, value)
                beta = min(beta, minvalue)
                if beta <= alpha:
                    break
            return minvalue

    def evaluation_function(self, node) -> int:  # return the evaluation value
        # TO DO
        eval = 1
        return eval

    def result(self, action: Action) -> Board:

        return state
