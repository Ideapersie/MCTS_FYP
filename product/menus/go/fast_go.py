from menus.go.goplayer import Player,Point
import numpy as np
import copy 

# Faster board implementation for MCTs rollouts using arrays 
class FastBoard: 
    def __init__(self, num_rows, num_cols, original_board=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        
        # Use numpy arrays to store board state, 0 for empty, 1 for black, 2 for white
        self.grid = np.zeros((num_rows+1, num_cols+1), dtype=int)
        
        # if original board is provided, copy the board state
        if original_board:
            for row in range(1, num_rows+1):
                for col in range(1, num_cols+1):
                    point = Point(row, col)
                    player = original_board.get_player(point)
                    # Use black: 1 and white: 2 to represent players
                    if player == Player.black:
                        self.grid[row,col] = 1
                    elif player == Player.white:
                        self.grid[row,col] = 2
         
    # Legal moves for simulation rollouts               
    def fast_legal_moves(self, next_player):
        moves = []
        for row in range(1, self.num_rows+1):
            for col in range(1, self.num_cols+1):
                # Skip occupied points
                if self.grid[row, col] != 0:
                    continue
                
                point = Point(row, col)
                
                # Skip if self capture
                if self.fast_self_capture(point, next_player):
                    continue
                # Add the legal move
                moves.append(point)
        return moves
         
    def fast_self_capture(self, point, player):
        # Converting enum values to grid values 
        player_num = 1 if player == Player.black else 2
        opponenet_num = 3 - player_num
        
        row, col = point.row, point.col

        # Check adjacent points for opponent stones
        adjacent_points = [
            (row-1, col), # up 
            (row+1, col), # down
            (row, col-1), # left
            (row, col+1)  # right
        ]
        
        # If adjacent positions is empty, not a self capture 
        for adj_row, adj_col in adjacent_points:
            if (1 <= adj_row <= self.num_rows and 
                1 <= adj_col <= self.num_cols and 
                self.grid[adj_row, adj_col] == 0):
                # Has liberties, not a self capture
                return False
                
    
        # Check if the stone capture any opponent stones
        for adj_row, adj_col in adjacent_points:
            # Skip if outside board
            if not (1 <= adj_row <= self.num_rows and 1 <= adj_col <= self.num_cols):
                continue
            
            # Check if adjecent point is an opponent stone and would be captured
            if self.grid[adj_row, adj_col] == opponenet_num and \
                self.has_no_liberties_except(adj_row, adj_col, row, col):
                # Capture the stone, therefore not a self capture
                return False
        # no liberties found and no captures -> self capture
        return True 
                        
    def has_no_liberties_except(self, stone_row, stone_col, except_row, except_col):
        # Check if the stone has any liberties except the exception point
        for adj_row, adj_col in [(stone_row-1, stone_col), (stone_row+1, stone_col), 
                                 (stone_row, stone_col-1), (stone_row, stone_col+1)]:
            # skip if outside the board
            if not (1 <= adj_row <= self.num_rows and 1 <= adj_col <= self.num_cols):
                continue
            # skip the except points
            if adj_row == except_row and adj_col == except_col:
                continue
            # if the adjacent point is empty, the stone has liberties
            if self.grid[adj_row, adj_col] == 0:
                return False
            
        # No liberties found
        return True