import copy 
from go.goplayer import Player,Point

class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign # bitwise XOR, returns True if exactly one is True
        self.point = point 
        self.is_play = (self.point is not None)
        self.is_pass = is_pass 
        self.is_resign = is_resign
        
    @classmethod
    def play(coor, point):
        return Move(point=point)
    
    @classmethod
    def pass_turn(coor):
        return Move(is_pass=True)
    
    @classmethod
    def resign(coor):
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
        
        
    def place_stone(self, player, point):
        if not self.in_grid(point):
            raise ValueError(f"Illegal move: The point {point} is outside the board's bound")
        
        if self._grid.get(point) is not None:
            raise ValueError(f"Illegal move: The point {point} is already occupied")
        
        same_colour_stones = [] 
        opposite_colour_stones = []
        liberties = []
        
        for neighbour in point.neighbours():
            # Skip neighbours which are out of bounds
            if not self.in_grid(neighbour):
                continue
            
            neighbour_string = self._grid.get(neighbour)
            
            if neighbour_string is None:
                liberties.append(neighbour)
            
            
            
            
        self._grid.add(point)
        