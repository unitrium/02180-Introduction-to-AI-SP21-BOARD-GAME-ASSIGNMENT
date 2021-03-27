"""Class implementing an artificial intelligence to play the game."""
from ..game import Player, Board


class AI(Player):
    """
    A player implementation controlled by an AI.
    max_depth: the maximum depth the AI will go in the search tree to find the best move.
    """
    max_depth: int
    times_iterated: int

    def __init__(self, white: bool, max_depth: int) -> None:
        super().__init__(white)
        self.max_depth = max_depth

    def receive(self, board: Board) -> None:
        """Call when its the palyer's turn, send him the state of the board."""
        self.times_iterated = 0
        list_actions = board.actions()
        eval_score = 0
        evalmax = 0
        best_action = list_actions[0]
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

    def alpha_beta_pruning(self, node: Board, current_depth: int,
                           alpha: int, beta: int, maximizingPlayer: bool) -> int:
        """Alpha beta pruning implementation."""
        self.times_iterated += 1
        # if node is a leaf node return evaluation value of the node
        if current_depth == self.max_depth or node.terminal_state():
            return self.eval(node)

        if maximizingPlayer:  # max part of the minimax
            maxvalue = float('-inf')
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
        openness_player = state.openness(black=not self.white)
        openness_opponent = state.openness(black=self.white)
        # since it returns as [white,black],
        score_player = scores[not self.white]
        score_opponent = scores[self.white]

        #print("Eval time taken:"+str(end-start))
        return (score_player - score_opponent) + (openness_player - openness_opponent)
