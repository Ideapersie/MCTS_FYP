import unittest
from go.goplayer import Player 
from go.goplayer import Point

class TestPlayer(unittest.TestCase):
    def test_other(self):
        # Testing the other property for both black and white players 
        
        self.assertEqual(Player.black.other, Player.white)
        self.assertEqual(Player.white.other, Player.black)
        
class TestPoint(unittest.TestCase):
    def test_point_tuple(self):
        point = Point(4,4)
        # Assert making sure, the row and col values are correct
        self.assertEqual(point.row, 4)
        self.assertEqual(point.col, 4)
    
    def test_point_neighbours(self):
        point = Point(4,4)
        
        neighbours = point.neighbours()
        # Expected neighbours
        expected_neighbours = [
            Point(3,4), # left
            Point(5,4), # right
            Point(4,3), # below
            Point(4,5), # above
        ]
        self.assertEqual(neighbours, expected_neighbours)
        
        
if __name__ == '__main__':
    unittest.main()