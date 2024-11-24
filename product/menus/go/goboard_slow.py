import copy 
from go.gotypes import Player

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