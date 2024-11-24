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
    
    