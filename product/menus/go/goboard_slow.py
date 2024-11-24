import copy 
from go.gotypes import Player

class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^is_resign # XoR operation 
        self.point = point 
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
        
    # Player places a stone on the board 
    @classmethod
    def play(cord, point):
        return Move(point=point)
    
    # Player passes turn to opponent 
    @classmethod 
    def pass_turn(cord):
        return Move(is_pass=True)
    
    # Player resigns 
    @classmethod
    def resign(cord):
        return Move(is_resign=True)
    
# GoStrings are chain of connected stones of same colour
class GoString():
    def __init__(self, colour, stones, liberties):
        self.colour = colour
        self.stones = stones
        self.liberties = liberties 
        
    # Liberty is any empty point touching a connected group 
    def remove_liberty(self, point):
        self.liberties.remove(point)
        
    def add_liberty(self, point):
        self.liberties.add(point)
        
    # Returns new Go string containing stones in both strings
    def merged_with(self, go_string):
        assert go_string.colour == self.colour
        combined_stones = self.stones | go_string.stones
        
        # Combined liberties excluding any stones in combined stones
        return GoString(self.colour, combined_stones, 
                        (self.liberties | go_string.liberties)- combined_stones) 
        
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self,other):
        return isinstance(other, GoString) and \
            self.colour == other.colour and \
            self.stones == other.stones and  \
            self.liberties == other.liberties
            
class Board():
    # Can specify number of rows and columns 
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows 
        self.num_cols = num_cols
        self._grid = {}
        
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and  \
            1 <= point.col <= self.num_cols
    
    # Returns a player is stone on that point else None   
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.colour
    
    # Returns entire string on stones at the point else None
    def get_go_string(self,point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string
        
    def place_stone(self, player, point):
        # Checks if point is on the grid and has not been played yet
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None 
        
        adjacent_same_colour = []
        adjacent_opposite_colour = []
        liberties = []
        
        for neighbour in point.neighbours():
            if not self.is_on_grid(neighbour):
                continue
            neighbour_string = self._grid.get(neighbour)
            
            if neighbour_string is None:
                liberties.append(neighbour)
            elif neighbour_string.colour == player:
                if neighbour_string not in adjacent_same_colour:
                    adjacent_same_colour.append(neighbour_string)
            else:
                if neighbour_string not in adjacent_opposite_colour:
                    adjacent_opposite_colour.append(neighbour_string)
        
        new_string = GoString(player, [point], liberties)
        
        # Merges string of the same colour
        for same_colour_string in adjacent_same_colour:
            new_string = new_string.merged_with(same_colour_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
            
        # Reduces liberties of adjacent strings of opposite colour
        for other_colour_string in adjacent_opposite_colour:
            other_colour_string.remove_liberty(point)
            
        # Remove opposite-colour strings with 0 liberties 
        for other_colour_string in adjacent_opposite_colour:
            if other_colour_string.num_liberties == 0:
                self._remove_string(other_colour_string)
                
    # Removing a string however also creating liberties for other strings
    def _remove_string(self, string):
        for point in string.stones:
            for neighbour in point.neighbours():
                neighbour_string = self._grid.get(neighbour)
                if neighbour_string is None:
                    continue
                if neighbour_string is not string:
                    neighbour_string.add_liberty(point)
                    
            self._grid[point] = None
            
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board 
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move
        
    # Returns new GameState after applying move
    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board) # creates copy of compound object
            next_board.place_stone(self.next_player, move.point)
            
        else:
            next_board = self.board 
        return GameState(next_board, self.next_player, move.point)
    
    @classmethod
    def new_game(cord, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
            
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
    
    # Deciding when the game is over 
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False 
        return self.last_move.is_pass and second_last_move.is_pass
    
    # Enforcing a self-capture rule
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        
        return new_string.num_liberties == 0
    
    # Implementing the ko rule 
    @property
    def situation(self):
        return (self.next_player, self.board)
    
    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False 
        
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False 
    
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and 
            not self.does_move_violate_ko(self.next_player, move)
        )