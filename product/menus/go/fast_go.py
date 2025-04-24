from menus.go.goplayer import Player,Point
from menus.go.go_moves import Move
import numpy as np
import copy 

# Faster board implementation for MCTs rollouts using arrays 
class FastBoard: 
    def __init__(self, num_rows, num_cols, original_board=None, game_state=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.game_state = game_state
        
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
                
                # Skip if ko rule
                if self.fast_ko_rule(point, next_player):
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
            
        # Simulate playing next move 
        original_grid = self.grid.copy()
        self.grid[row, col] = player_num
        
        # Check if this move would create group with no liberties
        has_liberty = self.group_has_liberty(row, col, player_num)
        
        if has_liberty:
            # Restore the original grid
            self.grid = original_grid
            return False
        
        # Check if this move would capture opponent stones
        would_capture = False
        
        # Check if move captures opponent stones
        for adj_row, adj_col in adjacent_points:
            # Check if inside board 
            if (1 <= adj_row <= self.num_rows and 1 <= adj_col <= self.num_cols and 
                self.grid[adj_row, adj_col] == opponenet_num):
                # Check opponent stone has liberties
                opponenent_liberty = self.group_has_liberty(adj_row, adj_col, opponenet_num)
                
                if not opponenent_liberty:
                    # Capture the opponent stone
                    would_capture = True
                    break
        
        # Restore the original grid        
        self.grid = original_grid
        
        return not would_capture
        
        
    # Loop and check for liberties in the group
    def group_has_liberty(self, start_row, start_col, player_num):
        visited = set([(start_row, start_col)])
        queue = [(start_row, start_col)]
        
        while queue:
            row, col = queue.pop(0)
            
            for adj_row, adj_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
                # Skip if adjacent point is outside the board 
                if not (1 <= adj_row <= self.num_rows and 1 <= adj_col <= self.num_cols):
                    continue
                # Skip if adjacent point is visited
                if (adj_row, adj_col) in visited:
                    continue
                
                # If adjacent point is empty, there is a liberty
                if self.grid[adj_row, adj_col] == 0:
                    return True
                
                # Add adjacent point to the queue if it is the same player
                if self.grid[adj_row, adj_col] == player_num:
                    visited.add((adj_row, adj_col))
                    queue.append((adj_row, adj_col))
                    
        # No liberties in group
        return False
    
    # Check if the move violates Ko rule
    def fast_ko_rule(self, point, player):
        
        # Check if game_state is None (first move) 
        if self.game_state is None or self.game_state.last_captured is None:
            return False
    
        """
        Ko rule only applies if:
        1. Playing a stone on the same point as the last captured stone
        2. Last capture was a single stone
        3. The stone placing will immediately capture that stone
        """
        row, col = point.row, point.col
        last_cap_row, last_cap_col = self.game_state.last_captured
        
        print(f"Checking ko rule: {row}, {col} vs {last_cap_row}, {last_cap_col}")
        
        # If this matches the last captured position, it may violate the ko rule
        return row == last_cap_row and col == last_cap_col
        
        
# Faster game state implementation for MCTs simulations
class FastGoState:
    def __init__(self, board_size, original_state=None):
        if original_state:
            self.board = FastBoard(board_size, board_size, original_state.board, self)
            self.next_player = original_state.next_player
            self.captured = original_state.captured.copy()
            self.last_captured = original_state.last_captured if hasattr(original_state, 'last_captured') else None
        
        else:
            self.board = FastBoard(board_size, board_size, game_state=self)
            self.next_player = Player.black
            self.captured = {Player.black: 0, Player.white: 0}
            # Explicitly initialize to None
            self.last_captured = None
            
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
        
        # Reset last captured stone
        self.last_captured = None
        
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
            captured, num_captured, captured_points = self.check_and_remove_group(adj_row, adj_col)
            
            # Only update if we actually captured something
            if captured and num_captured > 0:
                total_captures += num_captured
                
                # If exactly one stone was captured, store its position for ko rule
                if num_captured == 1:
                    # Store as a tuple, not a Point object
                    self.last_captured = captured_points[0]
                
        return total_captures
        
        
    # Check for captures and remove the captured stones
    def check_and_remove_group(self, row, col):
        # Check if the point is empty
        stone_colour = self.board.grid[row, col]
        if stone_colour == 0:
            return False, 0, []
        
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
            # Convert to list for easier handling
            captured_points = list(group)
            # Remove the captured group
            for captured_row, captured_col in group:
                self.board.grid[captured_row, captured_col] = 0
                
            return True, len(group), captured_points
        
        return False, 0, []
    
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
    
    # Get total of stones played 
    def get_total_moves(self):
        # count stones 
        black_stones = np.sum(self.board.grid == 1)
        white_stones = np.sum(self.board.grid == 2)
        
        # count captured stones
        total_captures = self.captured[Player.black] + self.captured[Player.white]
        
        # combine stones and captures
        return black_stones + white_stones + total_captures     