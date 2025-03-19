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
         
    
                
                        
