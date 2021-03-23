"""Class implementing an artificial intelligence to play the game."""
from code.game import board
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
                Board.board_from_move(board, a), 0, float('-inf'), float('inf'), True)
            if eval_score > evalmax:  # if it's the best value
                evalmax = eval_score
                best_action = a  # we can take this action which is the best

        if board.receive(best_action):  # Send to the board the best action
            print("IA move")
        else:
            raise Exception("Board has not accepted move by the AI.")

    def alpha_beta_pruning(self, node: Board, current_depth: int, alpha: int, beta: int, maximizingPlayer: bool) -> int:
        """Alpha beta pruning implementation."""
        # if node is a leaf node return evaluation value of the node
        if current_depth == self.max_depth or node.terminal_state():
            return self.evaluation_function(node)

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
        """Evaluate a state for a the player."""
        scores = state.calculate_players_total_block_size()
        if state.terminal_state():
            if self.white and scores[0] > scores[1] or not self.white and scores[0] < scores[1]:
                return float('inf')
            elif scores[0] == scores[1]:
                return 0
            return float('-inf')
        openess_player = state.openness(self.white)
        openess_openent = state.openness(not self.white)
        score_player = scores[int(not self.white)]
        score_openent = scores[int(self.white)]
        return score_player - score_openent + openess_player - openess_openent

    def result(self, action: Action) -> Board:

        return state
