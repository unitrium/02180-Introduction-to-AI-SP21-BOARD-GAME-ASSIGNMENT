# Class for the board of the game
from typing import List, Optional
from copy import deepcopy

from .player import Player, Action
import time


class Board:
    """A board the players can interact with.
    Initially empty.
    State: A matrix representing the board, None means the cell is free,
    0 is occupied by a white tile, 1 by a black tile.
    """
    state: List[List[Optional[int]]]
    size: int

    def __init__(self, size: int = 11, winning_rule: int = 2) -> None:
        self.size = size
        self.rule = winning_rule
        self.state = [[None for _ in range(size)] for _ in range(size)]

    def __copy__(self) -> "Board":
        """Return a deepcopy of the current instance."""
        new_board = Board(self.size, self.rule)
        new_board.state = deepcopy(self.state)
        return new_board

    def send(self, player: Player) -> None:
        """Send the state of the board to the player."""
        player.receive(self)

    def receive(self, move: Action) -> bool:
        """Receive a move from a player.
        :return: Whether the move has been accepted."""
        if not self._check_integrity(move):
            return False
        self.update_state(move)
        return True

    def update_state(self, move: Action):
        self.state[move.y][move.x] = 0
        x, y = move.direction_position()
        self.state[y][x] = 1

    def terminal_state(self) -> bool:
        """Determine whether the game is over."""
        for y, line in enumerate(self.state):
            for x, tile in enumerate(line):
                if tile is None:
                    for direction in self._free_neighbors(x, y):
                        return False
        return True
        # return len(self.actions()) == 0

    def _check_integrity(self, move: Action) -> bool:
        """Whether a move is acceptable by the current board."""
        if move.y < 0 or move.x < 0 or move.y >= self.size or move.x >= self.size:
            return False
        if not self.state[move.y][move.x] is None:
            return False
        if move.direction not in self._free_neighbors(move.x, move.y):
            return False
        return True

    def calculate_players_total_block_size(self):
        """Calculates the number of connected tiles for each color."""
        white_block_sizes = [0] * self.rule
        black_block_sizes = [0] * self.rule
        # Initialize array of booleans to check frontiers
        visited_tiles = []
        for _ in range(self.size):
            visited_tiles.append([False] * self.size)

        for i, line in enumerate(self.state):
            for j, tile in enumerate(line):
                if not tile is None:
                    block_size = self._calculate_block_size(
                        visited_tiles, i, j, tile)
                    temp_blocks = white_block_sizes
                    if tile == 1:
                        temp_blocks = black_block_sizes
                    lowest_current_block = temp_blocks[0]
                    lowest_current_block_index = 0
                    for n in range(1, len(temp_blocks)):
                        if lowest_current_block > temp_blocks[n]:
                            lowest_current_block = temp_blocks[n]
                            lowest_current_block_index = n
                    if block_size > lowest_current_block:
                        temp_blocks[lowest_current_block_index] = block_size
        return [sum(white_block_sizes), sum(black_block_sizes)]

    def declare_winner(self) -> None:
        """Declares a winner."""
        res = self.calculate_players_total_block_size(self)
        white_total_blocks = res[0]
        black_total_blocks = res[1]
        print("Game ended with the following score: ")
        print(
            f"  - White finished the game totalling a {white_total_blocks} block size.")
        print(
            f"  - Black finished the game totalling a {black_total_blocks} block size.")
        if white_total_blocks > black_total_blocks:
            print(
                "White has the highest total amount of blocks, and therefore is the winner!")
        elif black_total_blocks > white_total_blocks:
            print(
                "Black has the highest total amount of blocks, and therefore is the winner!")
        else:
            print(
                "Both players has the same total amount of blocks, and therefore it's a draw!")

    def _calculate_block_size(self, visited_tiles, x: int, y: int, color: int) -> int:
        """Counts the number of connected tiles."""
        if visited_tiles[x][y] == True:
            return 0
        if self.state[x][y] != color:  # If its not the same color, return.
            return 0
        visited_tiles[x][y] = True
        current_block = 1
        # Check all nearby neighbors
        if x - 1 > 0:
            current_block += self._calculate_block_size(
                visited_tiles, x-1, y, color)
        if x + 1 < self.size:
            current_block += self._calculate_block_size(
                visited_tiles, x+1, y, color)
        if y - 1 > 0:
            current_block += self._calculate_block_size(
                visited_tiles, x, y-1, color)
        if y + 1 < self.size:
            current_block += self._calculate_block_size(
                visited_tiles, x, y+1, color)
        return current_block

    def actions(self) -> List[Action]:
        """Computes all the possible actions."""
        actions = []
        for y, line in enumerate(self.state):
            for x, tile in enumerate(line):
                if tile is None:
                    for direction in self._free_neighbors(x, y):
                        actions.append(Action(x, y, direction))
        return actions

    def openness(self, white: bool) -> int:
        """Checks how many open positions are next to each color."""
        openness = 0
        for y, line in enumerate(self.state):
            for x, cell in enumerate(line):
                if cell == white:
                    openness += len(self._free_neighbors(x, y))
        return openness

    def _free_neighbors(self, x: int, y: int) -> List[int]:
        """Returns the free adjacents directions 0 up, 1 right, 2 down, 3 left."""
        neighbors = []
        if (not y == 0) and self.state[y-1][x] is None:
            neighbors.append(0)
        if (not x == (self.size - 1)) and self.state[y][x+1] is None:
            neighbors.append(1)
        if (not y == (self.size - 1)) and self.state[y+1][x] is None:
            neighbors.append(2)
        if (not x == 0) and self.state[y][x-1] is None:
            neighbors.append(3)
        return neighbors

    @staticmethod
    def board_from_move(board: "Board", action: Action) -> Optional["Board"]:
        """Create a new board from a move."""
        new_board = board.__copy__()
        new_board.update_state(action)
        return new_board
