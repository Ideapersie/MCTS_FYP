import unittest

from go.goplayer import Point, Player
from go.goboard import Move, GoString, Board

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
        self.str1 = GoString(Player.black, {(1,1)}, {(1,2),(2,1)})
        self.str2 = GoString(Player.black, {(2,1),(2,2)},{(1,1),(1,2),(2,3),(3,2),(3,1)})
        self.str3 = GoString(Player.white, {(3,3)},{(2,3),(4,3),(3,4),(3,2)})
        
    def test_init(self):
        self.assertEqual(self.str1.colour, Player.black)
        self.assertEqual(self.str1.stones, {(1,1)})
        self.assertEqual(self.str1.liberties, {(1,2),(2,1)})
    
    def test_add_liberty(self):
        self.str1.add_liberty((1,2))
        self.assertIn((1,2), self.str1.liberties)
        
    def test_remove_liberty(self):
        self.str1.remove_liberty((1,2))
        self.assertNotIn((1,2), self.str1.liberties)
        
    # Test combinining connected stones 
    def test_merged_with(self):
        merged_string = self.str1.merged_with(self.str2)
        expected_stones = {(1,1),(2,1),(2,2)}
        expected_liberties = {(1,2),(2,3),(3,2),(3,1)}
        
        self.assertEqual(merged_string.colour, Player.black)
        self.assertEqual(merged_string.stones, expected_stones)
        self.assertEqual(merged_string.liberties, expected_liberties)
        
    def test_num_liberties(self):
        self.assertEqual(self.str1.num_liberties, 2)
        self.assertEqual(self.str2.num_liberties, 5)
        
    def test_equal(self):
        str1_dup = GoString(Player.black, {(1,1)}, {(1,2),(2,1)})
        
        self.assertEqual(self.str1, str1_dup)
    
class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(9,9)

    # Testing board dimensions 
    def test_init(self):
    
        self.assertEqual(self.board.num_rows, 9)
        self.assertEqual(self.board.num_cols, 9)
       
    # Testing if the point is on the grind  
    def test_in_grid(self):
        in_grid_point = Point(2,2)
        toolow_grid_point = Point(0,0)
        toohigh_grid_point = Point(10,9)
        
        self.assertTrue(self.board.in_grid(in_grid_point))
        self.assertFalse(self.board.in_grid(toolow_grid_point))
        self.assertFalse(self.board.in_grid(toohigh_grid_point))
        
    # Testing if the point is out of bounds and error exception 
    def test_stone_out_of_bounds(self):
        out_of_bounds_point = Point(10,10)
        
        with self.assertRaises(ValueError) as error_msg:
            self.board.place_stone(Player.black, out_of_bounds_point)
            
        self.assertEqual(
            str(error_msg.exception),
            "Illegal move: The point Point(row=10, col=10) is outside the board's bound"                 
        )
        
    def test_get(self):
        point = Point(4,4)
        get_point = self.board.get(point)
        
        self.assertTrue
        
        
    def test_place_stone(self):
        point = Point(4,4)
        
        self.board.place_stone(Player.black, point)
        self.assertIn(point, self.board._grid)
        self.assertEqual(self.board._grid[point].colour, Player.black)
        
        
if __name__ == '__main__':
    unittest.main()