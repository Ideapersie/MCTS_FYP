from menus.go.goplayer import Player,Point
from menus.go.go_moves import Move
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
            # Copying fast board
            if hasattr(original_board, 'grid'):
                self.grid = copy.copy(original_board.grid)
            # Copying regular board 
            else:
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
    
# Faster game state implementation for MCTs simulations
class FastGoState:
    def __init__(self, board_size, original_state=None):
        if original_state:
            self.board = FastBoard(board_size, board_size, original_state.board)
            self.next_player = original_state.next_player
            self.captured = original_state.captured.copy()
        else:
            self.board = FastBoard(board_size, board_size)
            self.next_player = Player.black
            self.captured = {Player.black: 0, Player.white: 0}
            
        self.last_move = None
        # Track if previous move is a pass
        self.previous_pass = False
        # Track if a player has resigned 
        self.is_resigned = False
        
    # Faster and more efficient play move implementation
    def fast_play_move(self, move):
        
        # Handling resignation 
        if move.is_resign:
            self.is_resigned = True
            self.last_move = move 
            
            return self
        
        # Handling pass
        if move.is_pass:
            # Track if previous move is also a pass
            self.previous_pass = (self.last_move and self.last_move.is_pass)
            self.last_move = move
            self.next_player = Player.white if self.next_player == Player.black else Player.black
            
            return self
        
        # Reset status of pass move 
        self.previous_pass = False
        
        # Array values
        player_num = 1 if self.next_player == Player.black else 2 
        
        # Place stone on board 
        row, col = move.point.row, move.point.col
        self.board.grid[row, col] = player_num
        
        # Handle captures
        captures = self.handle_captures(move.point)
        self.captured[self.next_player] += captures
        
        # Update the next player and last move
        self.next_player = Player.white if self.next_player == Player.black else Player.black
        self.last_move = move
        
        return self
    
    # Handle the capture and update capture score
    def handle_captures(self, point):
        player_num = 1 if self.next_player == Player.black else 2
        opponent_num = 3 - player_num
        # Track the number of captures
        total_captures = 0 
        
        # Check adjacent points for potential captures
        for adj_row, adj_col in [(point.row-1, point.col), (point.row+1, point.col), 
                                 (point.row, point.col-1), (point.row, point.col+1)]:
            
            # Skip if outside the board
            if not (1 <= adj_row <= self.board.num_rows and 1 <= adj_col <= self.board.num_cols):
                continue
            
            # Skip if not opponent stone
            if self.board.grid[adj_row, adj_col] != opponent_num:
                continue
            
            # Check for captures and update the total captures
            _, num_captured = self.check_and_remove_group(adj_row, adj_col)
            total_captures += num_captured
                
        return total_captures
        
        
    # Check for captures and remove the captured stones
    def check_and_remove_group(self, row, col):
        """
        Returns (is_captured, num_captured) 
        """
        stone_colour = self.board.grid[row, col]
        if stone_colour == 0:
            return False, 0
        
        # Use BFS to find connected group, checking liberties 
        group = set()
        group.add((row, col))
        queue = [(row, col)]
        has_liberties = False
        
        # Keep searching for connected stones
        while queue:
            # Get the current point
            cur_row, cur_col = queue.pop(0)
            
            # Check adjacent points
            for adj_row, adj_col in [(cur_row-1, cur_col), (cur_row+1, cur_col), 
                                     (cur_row, cur_col-1), (cur_row, cur_col+1)]:
                
                # Skip if outside the board
                if not (1 <= adj_row <= self.board.num_rows and 1 <= adj_col <= self.board.num_cols):
                    continue
                
                # Finding a liberty
                if self.board.grid[adj_row, adj_col] == 0:
                    has_liberties = True
                # Continue searching for connected stones
                elif self.board.grid[adj_row, adj_col] == stone_colour and (adj_row, adj_col) not in group:
                    group.add((adj_row, adj_col))
                    queue.append((adj_row, adj_col))
                    
        if not has_liberties:
            # Remove the captured group
            for captured_row, captured_col in group:
                self.board.grid[captured_row, captured_col] = 0
            return True, len(group)
        
        return False, 0
    
    # Moves signifying the game is over 
    def fast_game_over(self):
        
        if self.last_move is None:
            return False 
        # If player resigns, the game is over 
        if self.is_resigned: 
            return True
        # if both player passes, the game is over 
        if self.last_move.is_pass and self.previous_pass:
            return True
        
        # else game continues 
        return False