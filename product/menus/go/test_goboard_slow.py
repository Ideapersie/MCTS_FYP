import unittest

from go.gotypes import Point
from go.goboard_slow import Move
from go.goboard_slow import GoString

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
        
class TestGoString(unittest.TestCase):
    def setUp(self):
        self.str1 = GoString("black", {(1,1)}, {(1,2),(2,1)})
        self.str2 = GoString("black", {(2,1),(2,2)},{(1,1),(1,2),(2,3),(3,2),(3,1)})
        self.str3 = GoString("white", {(3,3)},{(2,3),(4,3),(3,4),(3,2)})
        
    def test_init(self):
        self.assertEqual(self.str1.colour, "black")
        self.assertEqual(self.str1.stones, {(1,1)})
        self.assertEqual(self.str1.liberties, {(1,2),(2,1)})
    
    def test_add_liberty(self):
        self.str1.add_liberty((1,2))
        self.assertIn((1,2), self.str1.liberties)
        
    def test_remove_liberty(self):
        self.str1.remove_liberty((1,2))
        self.assertNotIn((1,2), self.str1.liberties)
        
    def test_merged_with(self):
        merged_string = self.str1.merged_with(self.str2)
        expected_stones = {(1,1),(2,1),(2,2)}
        expected_liberties = {(1,2),(2,3),(3,2),(3,1)}
        
        self.assertEqual(merged_string.colour, "black")
        self.assertEqual(merged_string.stones, expected_stones)
        self.assertEqual(merged_string.liberties, expected_liberties)
        
    def test_num_liberties(self):
        self.assertEqual(self.str1.num_liberties, 2)
        self.assertEqual(self.str2.num_liberties, 5)
        
    def test_equal(self):
        str1_dup = GoString("black", {(1,1)}, {(1,2),(2,1)})
        
        self.assertEqual(self.str1, str1_dup)
        
if __name__ == '__main__':
    unittest.main()