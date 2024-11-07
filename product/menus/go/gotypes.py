import enum 
from collections import namedtuple

class Player(enum.Enum):
    black = 1 
    white = 2 
    
    @property 
    def other(self):
        if self == Player.white:
            return Player.Black 
        else: 
            return Player.white
        
        
# With namedtuple, can access the points using point.row instead of point[0] 
class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return  [
            Point(self.row - 1 , self.col),
            Point(self.row + 1 , self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]