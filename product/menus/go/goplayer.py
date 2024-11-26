import enum 
from collections import namedtuple

class Player(enum.Enum):
    black = 1 
    white = 2
    
    @property
    def other(self):
        if self == Player.white:
            return Player.black
        else:
            return Player.white 
        
class Point(namedtuple('Point', 'row col')):
    def neighbours(self):
        return [
            Point(self.row - 1, self.col), # left 
            Point(self.row + 1, self.col), # right 
            Point(self.row, self.col + 1), # above
            Point(self.row, self.col - 1), # below
        ]