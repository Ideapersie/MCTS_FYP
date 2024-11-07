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