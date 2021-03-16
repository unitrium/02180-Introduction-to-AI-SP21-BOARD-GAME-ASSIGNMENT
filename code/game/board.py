# Class for the board of the game
from typing import List, Optional, Tuple

from .player import Player


class Action:
    x: int
    y: int
    direction: int

    def __init__(self, x: int, y: int, direction: int) -> None:
        self.x = x
        self.y = y
        self.direction = direction


class Board:
    """A board the players can interact with.
    Initially empty.
    """
    state: List[List[Optional[int]]]
    size: int

    def __init__(self, size: int) -> None:
        self.size = size
        self.state = [[None for _ in range(size)] for _ in range(size)]

    def send(self, player: Player) -> None:
        """Send the state of the board to the player."""
        player.receive(self.state)

    def receive(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Receive a move from a player."""
        if not self._check_integrity(move):
            return False
        direction = move[1]
        x = move[0][0]
        y = move[0][1]
        self.state[x][y] = 0
        if direction == 0:
            self.state[x][y+1] = 1
        elif direction == 1:
            self.state[x+1][y] = 1
        elif direction == 2:
            self.state[x][y-1] = 1
        else:
            self.state[x-1][y] = 1
        return False

    def terminal_state(self) -> bool:
        """Determine whether the game is over."""
        return len(self.actions()) == 0

    def _check_integrity(self, move: Tuple[Tuple[int, int], int]) -> bool:
        """Whether a move is acceptable by the current board."""
        direction = move[1]
        x = move[0][0]
        y = move[0][1]

        if not self.state[x][y] is None:
            return False
        if direction not in self._free_neighbors():
            return False
        return True


    def _check_winner(self, state: List[List[int]]):
        BLOCKS_WINNING_RULE_COUNT = 3 #How many blocks to count for each player
        BOARD_SIZE_N = 11
        white_block_sizes = [0] * BLOCKS_WINNING_RULE_COUNT
        black_block_sizes = [0] * BLOCKS_WINNING_RULE_COUNT
        #Initialize array of booleans to check frontiers
        visited_tiles = []
        for i in range(11):
            visited_tiles.append([False] * 11)

        #Iterate over all tiles in state array
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != None:
                    block_size = self._calculate_block_size(state, visited_tiles, i, j, state[i][j])
                    temp_blocks = white_block_sizes
                    if state[i][j] == 1:
                        temp_blocks = black_block_sizes
                    lowest_current_block = temp_blocks[0]
                    lowest_current_block_index = 0
                    #Itereate over n-1 elements in list, to find lowest nubmer of block_size, and if it should insert the block_size into it
                    for n in range(1, len(temp_blocks)):
                        if lowest_current_block > temp_blocks[n]:
                            lowest_current_block = temp_blocks[n]
                            lowest_current_block_index = n
                    if block_size > lowest_current_block:
                        temp_blocks[lowest_current_block_index] = block_size
        white_total_blocks = 0
        for block_size in white_block_sizes:
            white_total_blocks += block_size
        black_total_blocks = 0
        for block_size in black_block_sizes:
            black_total_blocks += block_size
        print("Game ended with the following score: ")
        print("  - White finished the game with the following biggest blocks: "+str(white_block_sizes)+" totalling a "+str(white_total_blocks)+" block size.")
        print("  - Black finished the game with the following biggest blocks: "+str(black_block_sizes)+" totalling a "+str(black_total_blocks)+" block size.")
        if white_total_blocks > black_total_blocks:
            print("White has the highest total amount of blocks, and therefore is the winner!")
        elif black_total_blocks > white_total_blocks:
            print("Black has the highest total amount of blocks, and therefore is the winner!")
        else:
            print("Both players has the same total amount of blocks, and therefore it's a draw!")


    def _calculate_block_size(self, state: List[List[int]], visited_tiles, x: int, y: int, color: int) -> int:
        if visited_tiles[x][y] == True: #Has this node already been counted?
            return 0
        if state[x][y] != color: #If its not the same color, return.
            return 0
        visited_tiles[x][y] = True
        current_block = 1
        #Check all nearby neighbors
        if x - 1 > 0:
            current_block += self._calculate_block_size(state, visited_tiles, x-1, y, color)
        if x + 1 < len(state):
            current_block += self._calculate_block_size(state, visited_tiles, x+1, y, color)
        if y - 1 > 0:
            current_block += self._calculate_block_size(state, visited_tiles, x, y-1, color)
        if y + 1 < len(state):
            current_block += self._calculate_block_size(state, visited_tiles, x, y+1, color)
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

    def _free_neighbors(self, x: int, y: int) -> List[int]:
        """Returns the free adjacents directions 0 up, 1 right, 2 down, 3 left."""
        neighbors = []
        if not y == 0 and self.state[x][y-1] is None:
            neighbors.append(0)
        if not x == (self.size - 1) and self.state[x+1][y] is None:
            neighbors.append(1)
        if not y == (self.size - 1) and self.state[x][y+1] is None:
            neighbors.append(2)
        if not x == 0 and self.state[x-1][y] is None:
            neighbors.append(3)
        return neighbors

