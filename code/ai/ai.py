"""Class implementing an artificial intelligence to play the game."""
from ..game import Player, Board, Action
from typing import List


class AI(Player):
    """
    A player implementation controlled by an AI.
    max_depth: the maximum depth the AI will go in the search tree to find the best move.
    """
    max_depth: int
    times_iterated: int
    heuristics_edges: bool
    heuristics_neighbors: bool

    SCORE_WEIGHT = 3
    OPENNESS_WEIGHT = 1

    def __init__(self, white: bool, max_depth: int,
                 heuristics_edges: bool = False, heuristics_neighbors: bool = False
                 ) -> None:
        super().__init__(white)
        self.max_depth = max_depth
        self.turn = 0
        self.heuristics_edges = heuristics_edges
        self.heuristics_neighbors = heuristics_neighbors

    def receive(self, board: Board) -> None:
        """Call when it's the player's turn, send him the state of the board."""
        self.times_iterated = 0
        self.turn += 1
        list_actions = self.actions(board)
        eval_score = 0
        evalmax = 0
        best_action = list_actions[0]
        board.compute_openness()
        res = board.calculate_players_total_block_size()
        board.white_score = res[0]
        board.black_score = res[1]
        for action in list_actions:
            eval_score = self.alpha_beta_pruning(
                Board.board_from_move(board, action), 0, float('-inf'), float('inf'), True)
            if eval_score > evalmax:
                evalmax = eval_score
                best_action = action

        if board.receive(best_action):
            print("IA move")
        else:
            raise Exception("Board has not accepted move by the AI.")
        print(
            f"Best move: {evalmax} with: [{best_action.x},{best_action.y}] dir: {best_action.direction}")
        print(f"Times iterated through: {self.times_iterated}")

    def actions(self, board: Board) -> List[Action]:
        """Computes all the possible actions."""
        actions = []
        heuristic_actions = []
        for y, line in enumerate(board.state):
            for x, tile in enumerate(line):
                if tile is None:
                    for direction in board._free_neighbors(x, y):
                        action = Action(x, y, direction)
                        if self.turn < 10:
                            if self.move_heuristics(action, board):
                                heuristic_actions.append(action)
                        actions.append(action)
        return heuristic_actions if len(heuristic_actions) > len(actions)/10 else actions

    def move_heuristics(self, action: Action, board: Board) -> bool:
        """Uses heuristics to select some of the best moves and reduce the search space."""
        x, y = action.direction_position()
        if self.heuristics_edges:
            # A heuristic to consider playing in the edges first but not in corners.
            if self.white:
                if (action.x == 1 or action.x == board.size - 2) and not (action.y == 0 or action.y == board.size - 1):
                    return True
                if (action.y == 1 or action.y == board.size - 2) and not (action.x == 0 or action.x == board.size - 1):
                    return True
            else:
                if (x == 1 or x == board.size - 2) and not (y == 0 or y == board.size - 1):
                    return True
                if (y == 1 or y == board.size - 2) and not (x == 0 or x == board.size - 1):
                    return True
        if self.heuristics_neighbors:
            # A heuristic to consider cells next to a tile first
            if len(board.touch_color(action.x, action.y)) > 0 or len(board.touch_color(action.x, action.y, white=False)) > 0:
                return True
            if len(board.touch_color(x, y)) > 0 or len(board.touch_color(x, y, white=False)):
                return False
        return False

    def alpha_beta_pruning(self, node: Board, current_depth: int,
                           alpha: int, beta: int, maximizingPlayer: bool) -> int:
        """Alpha beta pruning implementation."""
        self.times_iterated += 1
        # if node is a leaf node return evaluation value of the node
        if current_depth == self.max_depth or node.terminal_state():
            res = self.eval(node)
            #print("EVAL: "+str(res))
            return res

        if maximizingPlayer:  # max part of the minimax
            maxvalue = float('-inf')
            for action in self.actions(node):
                value = self.alpha_beta_pruning(
                    Board.board_from_move(node, action), current_depth+1, alpha, beta, False)
                maxvalue = max(maxvalue, value)
                alpha = max(alpha, maxvalue)
                #print("ALPHA: "+str(alpha)+" BETA: "+str(beta))
                if beta <= alpha:
                    break
            return maxvalue
        else:
            minvalue = float('inf')  # min part of the minimax
            for action in self.actions(node):
                value = self.alpha_beta_pruning(
                    Board.board_from_move(node, action), current_depth+1, alpha, beta, True)
                minvalue = min(minvalue, value)
                beta = min(beta, minvalue)
                if beta <= alpha:
                    break
            return minvalue

    def eval(self, state: Board) -> int:
        """Evaluate a state for a the player."""
        if state.terminal_state():
            if self.white and state.white_score > state.black_score or not self.white and state.white_score < state.black_score:
                return float('inf')
            elif state.white_score == state.black_score:
                return 0
            return float('-inf')
        openness_player = state.white_openness if self.white else state.black_openness
        openness_opponent = state.white_openness if not self.white else state.black_openness
        score_player = state.white_score if self.white else state.black_score
        score_opponent = state.white_score if not self.white else state.black_score
        return (self.SCORE_WEIGHT * score_player - self.SCORE_WEIGHT * score_opponent) + self.OPENNESS_WEIGHT * (openness_player - openness_opponent)
