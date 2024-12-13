import copy 
from menus.go.goplayer import Player,Point

class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign # bitwise XOR, returns True if exactly one is True
        self.point = point 
        self.is_play = (self.point is not None)
        self.is_pass = is_pass 
        self.is_resign = is_resign
        
    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign=True)
    
# Go strings are same coloured stones which are connected
class GoString():
    def __init__(self, colour, stones, liberties):
        self.colour = colour
        self.stones = set(stones)
        self.liberties = set(liberties)
        
    def add_liberty(self, point):
        self.liberties.add(point)
        
    def remove_liberty(self, point):
        self.liberties.remove(point)
        
    # Connect 2 Go Strings together to form a bigger String 
    def merged_with(self, go_string):
        assert go_string.colour == self.colour
        
        combined_stones = self.stones | go_string.stones
        combined_liberties = (self.liberties | go_string.liberties) - combined_stones
        
        return GoString(self.colour, combined_stones, combined_liberties )
        
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.colour == other.colour and \
            self.stones == other.stones and \
            self.liberties == other.liberties
            
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
        
    def __str__(self):
        # Stores representation of each row 
        rows = []
        # Dynamically generate column labels based on the number of columns
        col_labels = []
        for i in range(self.num_cols):
            # Convert each unicode index to letter 
            col_label = chr(ord('A')+ i)
            col_labels.append(col_label)
        
        # start from the bottom and end on -1 to account for zero indexing 
        for row in range(self.num_rows, 0, -1):
            current_row = []
            for col in range(1, self.num_cols + 1):
                point = Point(row, col)
                string = self.get_go_string(point)
                
                if string is None:
                    current_row.append('.') # Using dot for empty point 
                elif string.colour == Player.black:
                    current_row.append('X') # Using X for black stones 
                elif string.colour == Player.white:
                    current_row.append('O') # Using O for white stones 
                    
            # Joining all strings in this row with spacing in between 
            rows.append(f"{row} "+" ".join(current_row))
        
        # Add space to align with the space 
        col_label_bottom = "  " + " ".join(col_labels) 
        
        # Joining each row seperated by a new line and alphabetical label for columns 
        final_board = '\n'.join(rows) + '\n' + col_label_bottom
        
        return final_board
    
    # Checking if the stone is in the board boundaries    
    def in_grid(self, point):
        # Too low 
        if point.row < 1 or point.col < 1:
            return False 
        # Too high 
        elif point.row > self.num_rows or point.col > self.num_cols:
            return False
        else:
            return True
    
    # Return player colour of stone on point else None 
    def get_player(self, point):
        stone_point = self._grid.get(point)
        if stone_point is None:
            return None
        else:
            return stone_point.colour
    
    # Return go string at a point else None 
    def get_go_string(self, point):
        string_point = self._grid.get(point)
        
        if string_point is None:
            return None 
        else: 
            return string_point
        
    # Removing a string, can create liberties for other string
    def _remove_string(self, string):
        for stone in string.stones:
            for neighbour in stone.neighbours():
                neighbour_string = self._grid.get(neighbour)
                if neighbour_string is None:
                    continue
                elif neighbour_string is not string:
                    neighbour_string.add_liberty(stone)
            self._grid[stone] = None
        
    # Placing a stone on the board & manages liberties of neighbouring stones    
    def place_stone(self, player, point):
        if not self.in_grid(point):
            raise ValueError(f"Illegal move: The point {point} is outside the board's bound")
        
        if self._grid.get(point) is not None:
            raise ValueError(f"Illegal move: The point {point} is already occupied")
        
        # stones neighbouring the new placed stone  
        same_colour_neighbours = [] 
        opposite_colour_neighbours = []
        liberties = []
        
        for neighbour in point.neighbours():
            # Skip neighbours which are out of bounds
            if not self.in_grid(neighbour):
                continue
            
            neighbour_string = self._grid.get(neighbour)
            
            if neighbour_string is None:
                liberties.append(neighbour)
            
            # If same coloured neighbours then append 
            elif neighbour_string.colour == player:
                if neighbour_string not in same_colour_neighbours:
                    same_colour_neighbours.append(neighbour_string)     
            else:
                if neighbour_string not in opposite_colour_neighbours:
                    opposite_colour_neighbours.append(neighbour_string)
                    
        placed_string = GoString(player, [point], liberties)
             
        # Merge Strings if connected to same coloured strings 
        for placed_string_same in same_colour_neighbours:
            placed_string = placed_string.merged_with(placed_string_same)
            
        # Update board grid with new merged string
        for placed_string_point in placed_string.stones:
            self._grid[placed_string_point] = placed_string
            
        # Reduce liberties of opponent's neighbouring strings, If 0 then remove it 
        for place_string_other in opposite_colour_neighbours:
            place_string_other.remove_liberty(point)
            if place_string_other.num_liberties == 0:
                self._remove_string(place_string_other)
         
    # For explored region used for calculate_territory method  
    def explore_region(self, start, visited):
        # Stack stores explored points 
        stack = [start]
        territory = set()
        borders = set()
        
        # Using DFS to explore the region 
        while stack:
            point = stack.pop()
            
            # Skip if point has been visited 
            if point in visited:
                continue
            # If not, mark point as visited 
            visited.add(point)
            
            # If point is empty, add it to territory
            if self.get_player(point) is None:
                territory.add(point)
                
                for neighbours in point.neighbours():
                    if self.in_grid(neighbours):
                        stack.append(neighbours)
            # If point occupied = border of the region 
            else:
                borders.add(point)
                
        return territory, borders
      
    # Calculates the territory for both players           
    def calculate_territory(self):
        # Territories of each player 
        black_territory = 0 
        white_territory = 0
        neutral_territory = 0
        
        # Set containing all visited points
        visited = set()
        
        # Iterate over all the points 
        for row in range(1, self.num_rows + 1):
            for col in range(1, self.num_cols + 1):
                point = Point(row,col)
                
                # Skip occupied on visited points 
                if point in visited or self.get_player(point) is not None:
                    continue
                
                # Explore region and gather the territory and borders of each point 
                territory, borders = self.explore_region(point, visited)
                
                # Checking if certain region is surrounded by ONLY black or white stones
                black_border = True
                white_border = True
                
                # Loop over border points
                for border in borders:
                    player = self.get_player(border)
                    if player == Player.black:
                        white_border = False
                    elif player == Player.white:
                        black_border = False
                    else:
                        black_border = False
                        white_border = False
                       
                # Iterate over points in each territory       
                for point in territory:
                    # Empty points inside the border
                    if self.get_player(point) is None: 
                        if black_border and not white_border:
                            black_territory += 1
                        elif white_border and not black_border:
                            white_territory += 1
                        else:
                            neutral_territory += 1
                    
        return black_territory, white_territory, neutral_territory
      
    # To compare board states, especially for the Ko rule          
    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        # Checking board dimensions
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            return False
        
        # Zero indexing while go uses 1-based indexing 
        for row in range(1, self.num_rows+1 ):
            for col in range(1, self.num_cols+1):
                point = Point(row, col)
                if self.get_go_string(point) != other.get_go_string(point):
                    return False
        return True
            
class GoState():
    def __init__(self, board, previous_state, last_move, next_player, captured):
        self.board = board 
        self.previous_state = previous_state
        self.last_move = last_move
        self.next_player = next_player
        self.captured = captured or {Player.black: 0, Player.white: 0}
        
    @classmethod
    def new_game(cls, board_size):
        # Set board_size to have same dimensions
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(board_size[0], board_size[1])
        
        # Player with black stone starts first 
        return GoState(
                board=board, 
                previous_state=None, 
                last_move=None, 
                next_player=Player.black,
                captured={Player.black: 0, Player.white: 0}
            )
    
    # Apply the move to the board state and captured strings
    def play_move(self, move):
        if move is not None and move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
            
            # Captured strings in the next move
            next_captured = self.captured.copy()
            captured_string = self.board.get_go_string(move.point)
            
            if captured_string is None:
                captured_string = []
            
            # Amount of captured string
            for string in captured_string:
                next_captured[self.next_player.other] += len(string.stones)

        else:
            next_board = self.board
            next_captured = self.captured.copy()
        
        # Updates each variable for next GoState    
        return GoState(
            board=next_board, 
            previous_state=self, 
            last_move=move, 
            next_player=self.next_player.other,
            captured=next_captured
        )
    
    # Moves signifying the game is over 
    def game_over(self):
        
        if self.last_move is None:
            return False 
        # If player resigns, the game is over 
        if self.last_move.is_resign: 
            return True
        
        previous_last_move = self.previous_state.last_move
        if previous_last_move is None:
            return False 
        # if both player passes, the game is over 
        return self.last_move.is_pass and previous_last_move.is_pass
    
    # Self-capture is when player places stone and it captures itself 
    def self_capture(self, player, move):
        next_board = copy.deepcopy(self.board)
        # if move is pass or resign, cant be self capture 
        if not move.is_play:
            return False 
        next_board.place_stone(player, move.point)
        # retrieve the string connected to the point
        next_string = next_board.get_go_string(move.point)
        # if next move, liberty = 0 it is a self capture
        return next_string.num_liberties == 0
    
    # Ko rule is when the current move returns the board to previous state 
    def ko_rule(self, player, move):
        # Ko rule does not apply to resign or pass moves
        if not move.is_play:
            return False 
        
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        past_state = self.previous_state
        
        # Compare only with previous state's board
        if past_state is not None:
            return past_state.board == next_board
        # If not previous state, then ko rule does not apply
        return False 
    
    def valid_move(self, move):
        if self.game_over():
            return False
        
        # Passes and resign move always valid 
        if move.is_resign or move.is_pass:
            return True 
        if (  
            self.board.get_player(move.point) is None and # Point must be empty 
            not self.self_capture(self.next_player, move) and # No-self capture 
            not self.ko_rule(self.next_player, move) # Does not violate ko-rule 
        ):
            return True 
        # Else, move is invalid 
        return False 
    
    # Calculates the final score, adding komi
    def final_score(self, komi=6.5):
        
        black_territory, white_territory, _ = self.board.calculate_territory()
        
        black_score = black_territory + self.captured[Player.black]
        
        # Add 6.5 komi for the white player
        white_score = white_territory + self.captured[Player.white] + komi
        
        return {"Black": black_score, "White": white_score}
    
if __name__ == "__main__":
    GoState.new_game(board_size=9)
    