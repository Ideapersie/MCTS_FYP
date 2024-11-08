import copy 
from go.gotypes import Player
from go.gotypes import Point

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
        self.liberty.remove(point)
        
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