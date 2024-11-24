import unittest
from go.goboard_slow import Move
from go.gotypes import Point

class TestMove(unittest.TestCase):
    def test_play(self):
        # Create test point (4, 4)
        point = Point(4,4)
        move = Move.play(point)
        
        # Assert the play move 
        self.assertTrue(move.is_play)
        self.assertFalse(move.is_pass)
        self.assertFalse(move.is_resign)
        self.assertEqual(move.point, point)
        
    def test_pass(self):
        # Create pass move
        move = Move.pass_turn()
        
        # Assert the pass move
        self.assertFalse(move.is_play)
        self.assertTrue(move.is_pass)
        self.assertFalse(move.is_resign)
        
    def test_resign(self):
        # Create resign move 
        move = Move.resign()
        
        # Assert resign move 
        self.assertFalse(move.is_play)
        self.assertFalse(move.is_pass)
        self.assertTrue(move.is_resign)
        
if __name__ == '__main__':
    unittest.main()